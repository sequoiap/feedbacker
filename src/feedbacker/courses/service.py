from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from feedbacker.auth.models import User
from feedbacker.auth.roles import UserRolesEnum
from feedbacker.auth.schemas import UserCreate
from feedbacker.database import DbSession
from feedbacker.config import (
    FEEDBACKER_JWT_SECRET,
    FEEDBACKER_JWT_ALG,
)

from .models import Course
from .schemas import CourseCreate


def get_course_by_id(db_session: DbSession, course_id: int) -> Course:
    course = db_session.execute(select(Course).filter(Course.id == course_id)).scalar()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


def create_course(db_session: DbSession, course_in: CourseCreate) -> Course:
    instructors = db_session.execute(select(User).filter(User.id.in_(course_in.instructor_ids))).scalars().all()
    students = db_session.execute(select(User).filter(User.id.in_(course_in.student_ids))).scalars().all()
    course = Course(
        name=course_in.name,
        description=course_in.description,
        instructors=instructors,
        students=students,
    )
    db_session.add(course)
    db_session.commit()
    return course
