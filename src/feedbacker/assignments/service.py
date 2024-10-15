from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from feedbacker.auth.service import User
from .models import Assignment
from . import schemas


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


def create(db: Session):
    pass


def delete(db: Session):
    pass


def get(db: Session):
    pass


def update(db: Session):
    pass
