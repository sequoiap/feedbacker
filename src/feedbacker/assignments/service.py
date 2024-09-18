from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_assignment(db: Session, assignment_id: int):
    # return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    pass


def create(db: Session):
    pass


def delete(db: Session):
    pass


def get(db: Session):
    pass


def update(db: Session):
    pass
