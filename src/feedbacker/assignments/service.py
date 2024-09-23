from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends

from feedbacker.auth.service import User
from . import models
from . import schemas


def get_assignment(db: Session, assignment_id: int):
    # return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    pass


def get_all_assignments(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(models.Assignment).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create(db: Session):
    pass


def delete(db: Session):
    pass


def get(db: Session):
    pass


def update(db: Session):
    pass
