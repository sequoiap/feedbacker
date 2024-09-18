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


class AssignmentPagination(Pagination):
    total: int
    items: list[AssignmentRead] = []
