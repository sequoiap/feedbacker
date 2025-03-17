from datetime import datetime
from typing import Literal

from feedbacker.models import FeedbackerBase, Pagination


class AssignmentBase(FeedbackerBase):
    pass


class AssignmentCreate(AssignmentBase):
    title: str
    description: str
    grading_policy: Literal["highest", "latest", "first", "average"]


class AssignmentUpdate(AssignmentBase):
    title: str
    description: str


class AssignmentRead(AssignmentBase):
    id: int
    title: str
    description: str
    content: str
    created_at: datetime
    updated_at: datetime
    due_date: datetime
    published: bool
    submission_limit: int
    allow_late_submissions: bool
    grading_policy: str
    order: int
    time_limit: int


class AssignmentPagination(Pagination):
    total: int
    items: list[AssignmentRead] = []


class AttemptBase(FeedbackerBase):
    pass


class AttemptCreate(AttemptBase):
    assignment_id: int
    user_id: int


class AttemptRead(AttemptBase):
    id: int
    assignment_id: int
    student_id: int
    created_at: datetime
    updated_at: datetime


class AttemptUpdate(AttemptBase):
    id: int
    submitted_at: datetime


class AttemptPagination(Pagination):
    total: int
    items: list[AttemptRead] = []
