from typing import Optional
from datetime import datetime

from pydantic import field_validator, Field

from feedbacker.models import FeedbackerBase, Pagination
from feedbacker.auth.schemas import UserRead


class CourseBase(FeedbackerBase):
    name: str
    code: str
    description: str


class CourseCreate(CourseBase):
    instructor_ids: list[int] = []
    student_ids: list[int] = []


class CourseRead(CourseBase):
    id: int
    created_at: datetime
    # updated_at: str
    instructors: list[UserRead]
    students: list[UserRead]


class CourseUpdate(CourseBase):
    pass
    # id: int
    # created_at: str
    # updated_at: str
    # instructors: list[UserRead]
    # students: list[UserRead]
