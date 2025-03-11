from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
from feedbacker.auth.roles import UserRolesEnum
from feedbacker.auth.service import CurrentUser, AuthorizedAPIUser
from feedbacker.config import templates
from feedbacker.database import DbSession

from .schemas import CourseCreate, CourseRead, CourseUpdate
from .service import get_course_by_id, get_all_courses, create_course


api_router = APIRouter()


@api_router.get("/")
async def get_courses(
    db_session: DbSession,
    current_user: CurrentUser,
    user_id: int = None,
) -> list[CourseRead]:
    """Get all courses."""
    return get_all_courses(db_session, user_id=user_id)


@api_router.post("/")
async def create_course(
    db_session: DbSession,
    current_user: CurrentUser,
    course_in: CourseCreate,
    authorize: bool = Depends(AuthorizedAPIUser([UserRolesEnum.instructor])),
) -> CourseRead:
    """Create a new course."""
    return create_course(db_session, course_in)


@api_router.get("/{course_id}")
async def get_course(
    db_session: DbSession,
    current_user: CurrentUser,
    course_id: int,
) -> CourseRead:
    """Get a course."""
    return get_course_by_id(db_session, course_id)


# @router.get("/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="assignment.html", context={"id": id}
#     )
