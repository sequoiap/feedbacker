from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column

from feedbacker.database import Base


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
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    instructors = relationship("User")
    students = relationship("User")
    # feedbacks = relationship("Feedback", back_populates="assignment")
