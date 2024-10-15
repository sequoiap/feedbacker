from datetime import datetime
from tracemalloc import start

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from feedbacker.database import Base
from feedbacker.auth.models import User
from feedbacker.courses.models import Course


class Assignment(Base):
    """Assignment model.
    
    Args:
        title: The assignment's title.
        description: The assignment's description.
        content: The assignment's page content in Markdown.
        created_at: The date and time the assignment was created (default now).
        updated_at: The date and time the assignment was updated (default now).
        due_date: The assignment's due date.
        submission_limit: The assignment's submission limit (default 1). Set to
            -1 for unlimited submissions.
        user_id: The assignment's user ID.
        grading_policy: The assignment's grading policy, either "highest",
            "latest", "first", or "average".
        ordering: The assignment's ordering, used to sort assignments for
            display (default 0).

    Attributes:
        user: The assignment's user.
        course: The assignment's course.
    """
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
    due_date: Mapped[datetime]
    submission_limit: Mapped[int] = mapped_column(default=1)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # grading_policy: Mapped[str]
    # ordering: Mapped[int] = mapped_column(default=0)

    user: Mapped[User] = relationship("User")#, back_populates="assignments")
    course: Mapped[Course] = relationship("Course", back_populates="assignments")


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    started_at: Mapped[datetime] = mapped_column(default=datetime.now)
    submitted_at: Mapped[datetime]

    user: Mapped[User] = relationship("User")
    assignment: Mapped[Assignment] = relationship("Assignment")
