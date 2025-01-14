from pathlib import Path
from uuid import uuid4
from datetime import datetime

import aiofiles
from fastapi import Depends, HTTPException, status, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from feedbacker.config import UPLOADS_DIR
from feedbacker.auth.service import User
from .models import (
    Assignment,
    Attempt,
    MultipleChoiceOption,
    MultipleChoiceProblem,
    MultipleChoiceResponse,
    MultipleSelectOption,
    MultipleSelectProblem,
    MultipleSelectResponse,
    TrueFalseProblem,
    TrueFalseResponse,
    FileProblem,
    FileResponse,
    FreeResponseProblem,
    FreeResponseResponse,
)
from .schemas import AttemptCreate


def get_assignment(db_session: Session, assignment_id: int) -> Assignment:
    # return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    assn = db_session.execute(select(Assignment).filter(Assignment.id == assignment_id)).scalar()
    if not assn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return assn


def get_all_assignments(db: Session, course_id: int = None) -> list[Assignment]: #, skip: int = 0, limit: int = 100):
    stmt = select(Assignment)
    if course_id is not None:
        stmt = stmt.where(Assignment.course_id == course_id)
    # stmt = stmt.offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_assignment(db: Session):
    pass


def delete_assignment(db: Session, assignment_id: int):
    stmt = select(Assignment).where(Assignment.id == assignment_id)
    assn = db.scalars(stmt).one()
    db.delete(assn)
    db.commit()


def update_assignment(db: Session):
    pass


def get_attempt(db: Session, attempt_id: int) -> Attempt:
    stmt = select(Attempt).where(Attempt.id == attempt_id)
    attempt = db.scalars(stmt).one()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
    return attempt


def create_attempt(db: Session, attempt_in: AttemptCreate) -> Attempt:
    attempt = Attempt(
        assignment_id=attempt_in.assignment_id,
        user_id=attempt_in.user_id,
    )
    db.add(attempt)
    db.commit()
    return attempt


async def process_attempt(db: Session, attempt_id: int, formdata) -> Attempt:
    attempt = get_attempt(db, attempt_id)
    assignment = attempt.assignment
    for problem in assignment.problems:
        if isinstance(problem, MultipleChoiceProblem):
            response = MultipleChoiceResponse(
                problem_id=problem.id,
                attempt_id=attempt.id,
                option_id=int(formdata[f"{problem.id}"]),
            )
        elif isinstance(problem, MultipleSelectProblem):
            answer_ids = [int(a) for a in formdata.getlist(f"{problem.id}")]
            answers = db.scalars(
                select(MultipleSelectOption)
                .where(MultipleSelectOption.id.in_(answer_ids))
            ).all()
            response = MultipleSelectResponse(
                problem_id=problem.id,
                attempt_id=attempt.id,
                answers=answers,
            )
        elif isinstance(problem, TrueFalseProblem):
            response = TrueFalseResponse(
                problem_id=problem.id,
                attempt_id=attempt.id,
                choice=formdata[f"{problem.id}"] == "true",
            )
        elif isinstance(problem, FileProblem):
            file: UploadFile = formdata[f"{problem.id}"]
            file_path = UPLOADS_DIR / f"{uuid4()}_{file.filename}"
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()  # async read
                await out_file.write(content)  # async write
            if file_path.stat().st_size == 0:
                Path(file_path).unlink()
                file_path = None
            response = FileResponse(
                problem_id=problem.id,
                attempt_id=attempt.id,
                file_path=file_path,
            )
        elif isinstance(problem, FreeResponseProblem):
            response = FreeResponseResponse(
                problem_id=problem.id,
                attempt_id=attempt.id,
                response=formdata[f"{problem.id}"],
            )
        else:
            raise ValueError(f"Unknown problem type: {problem.type}")
        db.add(response)

    attempt.submitted_at = datetime.now()
    db.add(attempt)
    db.commit()
    return attempt

    # print(formdata)
    # print(formdata.keys())
    # print(formdata.values())
    # for k in formdata.keys():
    #     print(formdata.getlist(k))
    # for k, v in formdata.multi_items():
    #     print(k, v)
