from typing import Annotated

from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

# from dispatch.database.core import DbSession
# from dispatch.database.service import CommonParameters, search_filter_sort_paginate
# from dispatch.auth.permissions import SensitiveProjectActionPermission, PermissionsDependency
# from dispatch.models import PrimaryKey

# from .models import (
#     CaseCostTypeCreate,
#     CaseCostTypePagination,
#     CaseCostTypeRead,
#     CaseCostTypeUpdate,
# )
# from feedbacker.config import templates
from feedbacker import auth
from feedbacker.database import DbSession

from .schemas import UserCreate, UserLogin, UserLoginResponse, UserRead, UserUpdate, UserPagination, Token
from .service import CurrentUser, get_all_users, get, create, authenticate_user

user_router = APIRouter()
auth_router = APIRouter()
# frontend = FastAPI(debug=True)
# frontend = APIRouter()


@user_router.get("/")
async def get_users(
    db_session: DbSession,
    current_user: CurrentUser,
# ) -> UserPagination:
) -> list[UserRead]:
    """Get all assignments."""
    # users = get_all_users(db_session)
    # return UserPagination(total=len(users), items=users)
    return get_all_users(db_session)


@user_router.get("/{user_id}")
def get_user(
    db_session: DbSession,
    current_user: CurrentUser,
    user_id: int
) -> UserRead:
    """Get a user."""
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )
    return user


@user_router.post("/")
async def create_user(
    user: UserCreate,
    db_session: DbSession,
) -> UserRead:
    """Create a new user."""
    user = create(db_session=db_session, user_in=user)
    return user


@auth_router.get("/me", response_model=UserRead)
def get_me(
    *,
    current_user: CurrentUser,
):
    return current_user


@auth_router.post("/token")
async def login_for_access_token(
    db_session: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = user.create_token()
    return Token(access_token=access_token, token_type="bearer")


# @auth_router.post("/login")
# async def login(
#     request: Request,
#     user: UserLogin,
#     db_session: DbSession,
# ) -> UserLoginResponse:
#     """Login user."""
#     pass


# @frontend.get("/", response_class=HTMLResponse)
# async def assignments(request: Request):
#     return templates.TemplateResponse(
#         request=request, name="assignment.html", context={}
#     )

# @router.get("/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="assignment.html", context={"id": id}
#     )
