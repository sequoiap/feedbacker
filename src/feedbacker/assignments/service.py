from uuid import uuid4
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from feedbacker.auth.service import User
from .models import Assignment, Attempt
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
