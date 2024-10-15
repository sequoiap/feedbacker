from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column

from feedbacker.database import Base

if TYPE_CHECKING:
    from feedbacker.assignments.models import Assignment


course_instrcutors = Table(
    "course_instructors",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id")),
    Column("instructor_id", Integer, ForeignKey("users.id")),
)


course_students = Table(
    "course_students",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id")),
    Column("student_id", Integer, ForeignKey("users.id")),
)


class Course(Base):
    """Course model.

    Args:
        code: The course's code.
        name: The course's name.
        description: The course's description.
        content: Homepage content written in Markdown.
        created_at: The date and time the course was created (default now).

    Attributes:
        instructors: The course's instructors.
        students: The course's students.
    """
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[Optional[str]]
    # content: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    # TODO: Add an updated_at field?

    instructors = relationship("User", secondary=course_instrcutors)
    students = relationship("User", secondary=course_students)
    assignments: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="course")
    # feedbacks = relationship("Feedback", back_populates="assignment")
