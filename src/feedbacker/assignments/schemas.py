from datetime import datetime

from feedbacker.models import FeedbackerBase, Pagination


class AssignmentBase(FeedbackerBase):
    title: str
    description: str


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(AssignmentBase):
    pass


class AssignmentRead(AssignmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    content: str


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
