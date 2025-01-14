import http
import json
import urllib
from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException, Request, Form, Security, Depends, UploadFile, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError, BaseModel, PrivateAttr
from jinja2 import Environment, FileSystemLoader
from myst_parser.parsers.docutils_ import to_html5_demo
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.routing import compile_path
from starlette.responses import Response, StreamingResponse, FileResponse
from starlette.datastructures import MutableHeaders

from feedbacker.assignments.service import get_all_assignments, get_assignment, get_attempt, create_attempt, process_attempt
from feedbacker.assignments.schemas import AttemptCreate
from feedbacker.exceptions import RequiresLoginException
from feedbacker.auth.models import User
from feedbacker.auth.service import authenticate_user, decode_token
from feedbacker.database import DbSession
from feedbacker.courses.service import get_all_courses, get_course_by_id, get_courses_for_user, get_courses_instructed_for_user
from .config import (
    STATIC_DIR,
    templates,
    AUTH_COOKIE_NAME,
    REFRESH_COOKIE_NAME,
)


# we create the ASGI for the frontend
frontend = FastAPI(openapi_url="")
frontend.add_middleware(GZipMiddleware, minimum_size=1000)
frontend.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


http_bearer = HTTPBearer()


class url_for_query:
    """Handles url_for but with query parameters.
    
    Parameters
    ----------
    request : Request
        The request object.
    name : str
        The name of the route.
    params : str
        The path parameters.

    Attributes
    ----------
    path : URL
        The path of the route.
    request : Request
        The request object.
    """
    def __init__(self, request: Request, name: str, **params: str) -> None:
        self.path = request.url_for(name, **params)
        self.request = request
    
    def query(self, **params: str) -> str:
        """Include query parameters in the URL.

        Parameters
        ----------
        params : str
            The query parameters.
        
        Returns
        -------
        str
            The URL with the query parameters.
        """
        parsed = list(urllib.parse.urlparse(str(self.path)))
        parsed[4] = urllib.parse.urlencode(params)
        return urllib.parse.urlunparse(parsed)


@frontend.exception_handler(RequiresLoginException)
async def requires_login_exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    # redirect_url = CustomURLProcessor().url_for(request, "login").include_query_params(next=request.url.path)
    redirect_url = url_for_query(request, "login").query(next=request.url.path)
    return RedirectResponse(redirect_url)


@frontend.middleware("http")
async def default_page(request: Request, call_next):
    response = await call_next(request)
    # if response.status_code == 404:
    #     if STATIC_DIR:
    #         return FileResponse(path.join(STATIC_DIR, "index.html"))
    if response.status_code == 401:
        return RedirectResponse(f"{request.url_for("login")}?next={request.url.path}")
    return response


@frontend.middleware("http")
async def create_auth_header(request: Request, call_next):
    # Authorization MUST be from a cookie
    auth_cookie = request.cookies.get(AUTH_COOKIE_NAME, None)
    # if "Authorization" not in request._headers:
    headers = MutableHeaders(request._headers)
    headers["Authorization"] = f"Bearer {auth_cookie}"
    request._headers = headers
    request.scope.update(headers=request.headers.raw)

    response = await call_next(request)
    return response


# TODO: Create middleware that adds the user to each response so that the
# account name can be displayed on each page's dropdown menu.


class LoginForm(BaseModel):
    username: str
    password: str


def authorize_user(db_session: DbSession, auth: HTTPAuthorizationCredentials = Security(http_bearer)) -> User:
    """User auth token dependency.
    
    Args:
        db_session (DbSession): The database session.
        auth (HTTPAuthorizationCredentials): The HTTP authorization credentials.

    Returns:
        The user model.

    Raises:
        RequiresLoginException: If the user is not logged in.
    """
    try:
        user = decode_token(db_session, auth.credentials)
        return user
    except Exception as e:
        raise RequiresLoginException()


class AuthorizedUser:
    """Check if a user has the required permissions.

    Based on https://dev.to/moadennagi/role-based-access-control-using-fastapi-h59.
    
    Examples:
        >>> @app.get('/items')
        ... def items(
        ...     authorize: bool = Depends(PermissionChecker(required_permissions=['items:read',]))
        ... ):
        ...     return 'items'
    """
    def __init__(self, required_permissions: list[str] = []) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: Annotated[User, Depends(authorize_user)]) -> User:
        if user.check_permissions(self.required_permissions):
            return user
        raise RequiresLoginException()


@frontend.get("/login", response_class=HTMLResponse)
async def login(request: Request, next: str = "/"):
    return templates.TemplateResponse(
        request=request,
        name="login.html.j2",
        context={
            "next": next,
        },
    )


@frontend.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    db_session: DbSession,
    form: Annotated[LoginForm, Form()],
    next: str = "/",
):
    if not (form.username and form.password):
        return templates.TemplateResponse(
            request=request,
            name="login.html.j2",
            context={
                "errors": ["Username and password are required."],
                "username": form.username,
                "password": form.password,
            },
        )
    else:
        user = authenticate_user(db_session, form.username, form.password)
        if not user:
            return templates.TemplateResponse(
                request=request,
                name="login.html.j2",
                context={
                    "errors": ["Incorrect username or password"],
                    "username": form.username,
                    "password": form.password,
                },
            )
        access_token = user.create_token()
        next = next or "/"
        response = RedirectResponse(next, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(AUTH_COOKIE_NAME, access_token, httponly=True)
        return response


@frontend.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(request.url_for("login"), status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(AUTH_COOKIE_NAME)
    response.delete_cookie(REFRESH_COOKIE_NAME)
    return response


@frontend.get("/", response_class=HTMLResponse)
async def index(
    db_session: DbSession,
    request: Request,
    refresh_courses: Optional[bool] = False,
    user: User = Depends(AuthorizedUser())
):
    courses = get_courses_for_user(db_session, user)
    instructed_courses = get_courses_instructed_for_user(db_session, user)
    if refresh_courses:
        print("Refreshing courses")
    return templates.TemplateResponse(
        request=request,
        name="index.html.j2",
        context={
            "courses": courses,
            "instructed_courses": instructed_courses,
        },
    )


@frontend.get("/courses/{course_id}", response_class=HTMLResponse)
async def course_home(
    course_id: int,
    db_session: DbSession,
    request: Request,
    user: User = Depends(AuthorizedUser()),
):
    course = get_course_by_id(db_session, course_id)
    return templates.TemplateResponse(
        request=request,
        name="course_home.html.j2",
        context={
            "course": course,
            "courses": get_all_courses(db_session),
            # "course_html": to_html5_demo(course.content),
        },
    )


@frontend.get("/courses/assignments", response_class=HTMLResponse)
async def assignments(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="assignments.html.j2",
        context={},
    )


@frontend.get("/courses/{course_id}/assignments", response_class=HTMLResponse)
async def assignments_for_course(
    course_id: int,
    db_session: DbSession,
    request: Request,
    user: User = Depends(AuthorizedUser()),
):
    return templates.TemplateResponse(
        request=request,
        name="assignments.html.j2",
        context={
            "course": get_course_by_id(db_session, course_id),
            "courses": get_all_courses(db_session),
            "assignments": get_all_assignments(db_session, course_id=course_id),
        },
    )


@frontend.get("/courses/{course_id}/assignments/{assignment_id}", response_class=HTMLResponse)
async def assignment_details(
    course_id: int,
    assignment_id: int,
    db_session: DbSession,
    request: Request
):
    assignment = get_assignment(db_session, assignment_id)
    return templates.TemplateResponse(
        request=request,
        name="assignment.html.j2", 
        context={
            "course": get_course_by_id(db_session, course_id),
            "assignment": assignment,
            "assignment_html": to_html5_demo(assignment.content),
            "courses": get_all_courses(db_session),
        },
    )


@frontend.get("/courses/{course_id}/assignments/{assignment_id}/edit", response_class=HTMLResponse)
async def edit_assignment_details(
    course_id: int,
    assignment_id: int,
    db_session: DbSession,
    request: Request
):
    assignment = get_assignment(db_session, assignment_id)
    return templates.TemplateResponse(
        request=request,
        name="assignment_edit.html.j2", 
        context={
            "course": get_course_by_id(db_session, course_id),
            "assignment": assignment,
            "assignment_html": to_html5_demo(assignment.content),
            "courses": get_all_courses(db_session),
        },
    )


@frontend.get("/courses/{course_id}/assignments/{assignment_id}/attempt", response_class=HTMLResponse)
async def begin_assignment_attempt(
    course_id: int,
    assignment_id: int,
    db_session: DbSession,
    request: Request,
    user: User = Depends(AuthorizedUser()),
):
    assignment = get_assignment(db_session, assignment_id)
    attempt_id = request.cookies.get("attempt_id")
    if attempt_id is not None:
        attempt = get_attempt(db_session, attempt_id)
    else:
        attempt = create_attempt(db_session, AttemptCreate(assignment_id=assignment_id, user_id=user.id))
    # return RedirectResponse(
    #     request.url_for("assignment_attempt", course_id=course_id, assignment_id=assignment_id, attempt_id=attempt)
    # )
    response = templates.TemplateResponse(
        request=request,
        name="attempt.html.j2",
        context={
            "course": get_course_by_id(db_session, course_id),
            "assignment": assignment,
            "assignment_html": to_html5_demo(assignment.content),
            "courses": get_all_courses(db_session),
            "attempt_id": attempt.id,
            "problems": assignment.problems,
        },
    )
    response.set_cookie("attempt_id", attempt.id)
    return response


@frontend.post("/courses/{course_id}/assignments/{assignment_id}/attempt", response_class=HTMLResponse)
async def submit_assignment_attempt(
    course_id: int,
    assignment_id: int,
    db_session: DbSession,
    request: Request,
):
    assignment = get_assignment(db_session, assignment_id)
    attempt_id = request.cookies.get("attempt_id")
    formdata = await request.form()
    attempt = await process_attempt(db_session, attempt_id, formdata)
    response = templates.TemplateResponse(
        request=request,
        formdata=formdata,
        name="grader.html.j2",
        context={
            "course": get_course_by_id(db_session, course_id),
            "assignment": assignment,
            "assignment_html": to_html5_demo(assignment.content),
            "courses": get_all_courses(db_session),
            "attempt_id": attempt_id,
        },
    )
    # response.delete_cookie("attempt_id")
    return response


@frontend.get("/courses/{course_id}/assignments/{assignment_id}/attempt/{attempt_id}", response_class=HTMLResponse)
async def assignment_attempt(
    course_id: int,
    assignment_id: int,
    attempt_id: str,
    db_session: DbSession,
    request: Request
):
    assignment = get_assignment(db_session, assignment_id)
    # attempt = get_attempt(db_session, attempt_id)
    response =  templates.TemplateResponse(
        request=request,
        name="attempt.html.j2",
        context={
            "course": get_course_by_id(db_session, course_id),
            "assignment": assignment,
            "assignment_html": to_html5_demo(assignment.content),
            "courses": get_all_courses(db_session),
            "attempt_id": attempt_id,
        },
    )
    response.set_cookie("attempt_id", attempt_id)
    return response


@frontend.get("/courses/{course_id}/grades", response_class=HTMLResponse)
async def course_grades(
    course_id: int,
    db_session: DbSession,
    request: Request,
    user: User = Depends(AuthorizedUser()),
):
    return templates.TemplateResponse(
        request=request,
        name="grades.html.j2",
        context={
            "course": get_course_by_id(db_session, course_id),
            "courses": get_all_courses(db_session),
        },
    )


@frontend.get("/urls")
async def list_urls(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    print(request)
    print(request.app)
    print(dir(request))
    return url_list
