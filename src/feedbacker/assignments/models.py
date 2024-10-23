from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from feedbacker.database import Base
from feedbacker.auth.models import User
from feedbacker.courses.models import Course
from feedbacker.grader import grade_file


# TODO: Cascade delete of problems when assignment is deleted
class Assignment(Base):
    """Assignment model.
    
    Args:
        title: The assignment's title.
        description: The assignment's description.
        content: The assignment's page content in Markdown.
        created_at: The date and time the assignment was created (default now).
        updated_at: The date and time the assignment was updated (default now).
        due_date: The assignment's due date.
        published: Whether the assignment is published (default False).
        submission_limit: The assignment's submission limit (default 1). Set to
            -1 for unlimited submissions.
        allow_late_submissions: Whether to allow late submissions (default False).
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
    # published: Mapped[bool] = mapped_column(default=False)
    submission_limit: Mapped[int] = mapped_column(default=1)
    # allow_late_submissions: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # grading_policy: Mapped[str]
    order: Mapped[int] = mapped_column(default=0)

    user: Mapped[User] = relationship("User")#, back_populates="assignments")
    course: Mapped[Course] = relationship("Course", back_populates="assignments")
    problems: Mapped[list["Problem"]] = relationship("Problem", back_populates="assignment")


class Attempt(Base):
    """Assignment attempt.

    Args:
        assignment_id: The attempt's assignment ID.
        user_id: The attempt's user ID.
        started_at: The attempt's start time (default now).
        submitted_at: The attempt's submission time, nullable.

    Attributes:
        user: The attempt's user.
        assignment: The attempt's assignment.
    """
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    started_at: Mapped[datetime] = mapped_column(default=datetime.now)
    submitted_at: Mapped[datetime] = mapped_column(nullable=True)

    user: Mapped[User] = relationship("User")
    assignment: Mapped[Assignment] = relationship("Assignment")


class Problem(Base):
    """Assignment problem.
    
    Args:
        assignment_id: The problem's assignment ID.
        type: The problem's type.
        text: The problem's text.
        order: The problem's order.
        points: The problem's points (default 1).

    Attributes:
        assignment: The problem's assignment.
    """
    __tablename__ = "problems"
    __mapper_args__ = {
        "polymorphic_identity": "problem",
        "polymorphic_on": "type",
    }

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[str] = mapped_column(index=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    text: Mapped[str] = mapped_column(default="")
    order: Mapped[int] = mapped_column(default=0)
    points: Mapped[float] = mapped_column(default=1.0)

    assignment: Mapped[Assignment] = relationship("Assignment", back_populates="problems")


class Response(Base):
    __tablename__ = "responses"
    __mapper_args__ = {
        "polymorphic_identity": "response",
        "polymorphic_on": "type",
    }
    __table_args__ = (
        UniqueConstraint('problem_id', 'attempt_id', name='uq_problem_attempt'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[str] = mapped_column(index=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    attempt_id: Mapped[int] = mapped_column(ForeignKey("attempts.id"))
    score: Mapped[float] = mapped_column(default=0.0)

    problem: Mapped[Problem] = relationship("Problem")
    attempt: Mapped[Attempt] = relationship("Attempt")


# multiple_choice_options = Table(
#     "multiple_choice_to_options_mapping",
#     Base.metadata,
#     Column("problem_id", Integer, ForeignKey("multiple_choice_problems.id")),
#     Column("option_id", Integer, ForeignKey("multiple_choice_options.id")),
# )


class MultipleChoiceOption(Base):
    __tablename__ = "multiple_choice_options"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("multiple_choice_problems.id"))
    text: Mapped[str]
    order: Mapped[int]

    problem: Mapped["MultipleChoiceProblem"] = relationship("MultipleChoiceProblem", back_populates="options", foreign_keys=[problem_id])


class MultipleChoiceProblem(Problem):
    __tablename__ = "multiple_choice_problems"
    __mapper_args__ = {
        "polymorphic_identity": "multiple_choice",
    }

    id: Mapped[int] = mapped_column(ForeignKey("problems.id"), primary_key=True)
    randomize_choices: Mapped[bool] = mapped_column(default=True)
    correct_choice_id: Mapped[int] = mapped_column(ForeignKey("multiple_choice_options.id"))

    options: Mapped[list["MultipleChoiceOption"]] = relationship(
        "MultipleChoiceOption",
        back_populates="problem",
        foreign_keys=[MultipleChoiceOption.problem_id]
    )
    correct_choice: Mapped[int] = relationship("MultipleChoiceOption", foreign_keys=[correct_choice_id])


class MultipleChoiceResponse(Response):
    __tablename__ = "multiple_choice_responses"
    __mapper_args__ = {
        "polymorphic_identity": "multiple_choice",
    }

    id: Mapped[int] = mapped_column(ForeignKey("responses.id"), primary_key=True, index=True)
    option_id: Mapped[int] = mapped_column(ForeignKey("multiple_choice_options.id"))

    option: Mapped[MultipleChoiceOption] = relationship("MultipleChoiceOption")
    problem: Mapped[MultipleChoiceProblem] = relationship("MultipleChoiceProblem")

    def grade(self) -> tuple[float, str]:
        if self.option_id == self.problem.correct_choice:
            self.score = self.problem.points
        return self.score, "Correct"


multiple_select_answers = Table(
    "multiple_select_answers",
    Base.metadata,
    Column("problem_id", Integer, ForeignKey("multiple_select_problems.id")),
    Column("answer_id", Integer, ForeignKey("multiple_select_options.id")),
)


class MultipleSelectOption(Base):
    __tablename__ = "multiple_select_options"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("multiple_select_problems.id"))
    text: Mapped[str]
    order: Mapped[int]

    problem: Mapped["MultipleSelectProblem"] = relationship("MultipleSelectProblem", back_populates="options", foreign_keys=[problem_id])


class MultipleSelectProblem(Problem):
    __tablename__ = "multiple_select_problems"
    __mapper_args__ = {
        "polymorphic_identity": "multiple_select",
    }

    id: Mapped[int] = mapped_column(ForeignKey("problems.id"), primary_key=True, index=True)
    randomize_choices: Mapped[bool] = mapped_column(default=True)
    partial_credit: Mapped[bool] = mapped_column(default=False)

    options: Mapped[list["MultipleSelectOption"]] = relationship("MultipleSelectOption", back_populates="problem", foreign_keys=[MultipleSelectOption.problem_id])
    answers: Mapped[list["MultipleSelectOption"]] = relationship("MultipleSelectOption", secondary=multiple_select_answers)


multiple_select_response_answers = Table(
    "multiple_select_response_answers",
    Base.metadata,
    Column("response_id", Integer, ForeignKey("multiple_select_responses.id")),
    Column("answer_id", Integer, ForeignKey("multiple_select_options.id")),
)

class MultipleSelectResponse(Response):
    __tablename__ = "multiple_select_responses"
    __mapper_args__ = {
        "polymorphic_identity": "multiple_select",
    }

    id: Mapped[int] = mapped_column(ForeignKey("responses.id"), primary_key=True, index=True)
    answers: Mapped[list["MultipleSelectOption"]] = relationship("MultipleSelectOption", secondary=multiple_select_response_answers)

    def grade(self) -> tuple[float, str]:
        correct_answers = set(self.problem.answers)
        selected_answers = set(self.answers)
        if correct_answers == selected_answers:
            self.score = self.problem.points
            feedback = "Correct"
        elif self.problem.partial_credit:
            self.score = self.problem.points * len(correct_answers & selected_answers) / len(correct_answers)
            feedback = "Partial credit"
        else:
            feedback = "Incorrect"
        return self.score, feedback


class TrueFalseProblem(Problem):
    __tablename__ = "true_false_problems"
    __mapper_args__ = {
        "polymorphic_identity": "true_false",
    }

    id: Mapped[int] = mapped_column(ForeignKey("problems.id"), primary_key=True)
    correct_choice: Mapped[bool] = mapped_column(index=True)


class TrueFalseResponse(Response):
    __tablename__ = "true_false_responses"
    __mapper_args__ = {
        "polymorphic_identity": "true_false",
    }

    id: Mapped[int] = mapped_column(ForeignKey("responses.id"), primary_key=True, index=True)
    choice: Mapped[bool] = mapped_column(index=True)

    def grade(self) -> tuple[float, str]:
        if self.choice == self.problem.correct_choice:
            self.score = self.problem.points
            feedback = "Correct"
        else:
            feedback = "Incorrect"
        return self.score, feedback


class FreeResponseProblem(Problem):
    __tablename__ = "free_response_problems"
    __mapper_args__ = {
        "polymorphic_identity": "free_response",
    }

    id: Mapped[int] = mapped_column(ForeignKey("problems.id"), primary_key=True)


class FileProblem(Problem):
    __tablename__ = "file_problems"
    __mapper_args__ = {
        "polymorphic_identity": "file",
    }

    id: Mapped[int] = mapped_column(ForeignKey("problems.id"), primary_key=True)
    grader_script: Mapped[str] = mapped_column(index=True)


class FileResponse(Response):
    __tablename__ = "file_responses"
    __mapper_args__ = {
        "polymorphic_identity": "file",
    }

    id: Mapped[int] = mapped_column(ForeignKey("responses.id"), primary_key=True, index=True)
    file_path: Mapped[str]

    def grade(self) -> tuple[float, str]:
        output, status = grade_file(self.problem.grader_script, [self.file_path])
        self.score = status["score"]
        return self.score, output
