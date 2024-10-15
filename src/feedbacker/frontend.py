from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from jinja2 import Environment, FileSystemLoader
from myst_parser.parsers.docutils_ import to_html5_demo
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.routing import compile_path
from starlette.responses import Response, StreamingResponse, FileResponse

from feedbacker.assignments.service import get_all_assignments, get_assignment
from feedbacker.database import DbSession
from feedbacker.courses.service import get_all_courses, get_course_by_id
from .config import (
    STATIC_DIR,
    templates,
)


# we create the ASGI for the frontend
frontend = FastAPI(openapi_url="")
frontend.add_middleware(GZipMiddleware, minimum_size=1000)
frontend.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@frontend.middleware("http")
async def default_page(request, call_next):
    response = await call_next(request)
    # if response.status_code == 404:
    #     if STATIC_DIR:
    #         return FileResponse(path.join(STATIC_DIR, "index.html"))
    return response


@frontend.get("/", response_class=HTMLResponse)
async def index(db_session: DbSession, request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html.j2",
        context={
            "courses": get_all_courses(db_session),
        },
    )


@frontend.get("/{course_id}", response_class=HTMLResponse)
async def course_home(course_id: int, db_session: DbSession, request: Request):
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


@frontend.get("/assignments", response_class=HTMLResponse)
async def assignments(request: Request):
    return templates.TemplateResponse(
        request=request, name="assignments.html.j2", context={}
    )


@frontend.get("/{course_id}/assignments", response_class=HTMLResponse)
async def assignments_for_course(course_id: int, db_session: DbSession, request: Request):
    return templates.TemplateResponse(
        request=request,
        name="assignments.html.j2", 
        context={
            "course": get_course_by_id(db_session, course_id),
            "courses": get_all_courses(db_session),
            "assignments": get_all_assignments(db_session, course_id=course_id),
        },
    )


@frontend.get("/{course_id}/assignments/{assignment_id}", response_class=HTMLResponse)
async def assignment_details(course_id: int, assignment_id: int, db_session: DbSession, request: Request):
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


@frontend.get("/{course_id}/assignments/{assignment_id}/edit", response_class=HTMLResponse)
async def edit_assignment_details(course_id: int, assignment_id: int, db_session: DbSession, request: Request):
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


@frontend.get("/{course_id}/assignments/{assignment_id}/attempt", response_class=HTMLResponse)
async def assignment_attempt(course_id: int, assignment_id: int, db_session: DbSession, request: Request):
    assignment = get_assignment(db_session, assignment_id)
    return templates.TemplateResponse(
        request=request,
        name="attempt.html.j2", 
        context={
            "course": get_course_by_id(db_session, course_id),
            "assignment": assignment,
            "assignment_html": to_html5_demo(assignment.content),
            "courses": get_all_courses(db_session),
        },
    )


@frontend.get("/{course_id}/grades", response_class=HTMLResponse)
async def course_grades(course_id: int, db_session: DbSession, request: Request):
    return templates.TemplateResponse(
        request=request,
        name="grades.html.j2",
        context={
            "course": get_course_by_id(db_session, course_id),
            "courses": get_all_courses(db_session),
        },
    )
