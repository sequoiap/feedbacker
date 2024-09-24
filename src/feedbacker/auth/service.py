from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from feedbacker.auth.roles import UserRolesEnum
from feedbacker.auth.schemas import UserCreate
from feedbacker.database import DbSession
from feedbacker.config import (
    FEEDBACKER_JWT_SECRET,
    FEEDBACKER_JWT_ALG,
)

from .models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(db_session: DbSession, username: str, password: str) -> User | bool:
    user = get_by_username(db_session, username)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user


async def get_current_user(db_session: DbSession, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, FEEDBACKER_JWT_SECRET, algorithms=[FEEDBACKER_JWT_ALG])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_by_username(db_session, username=username)
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_role(
    request: Request,
    current_user: CurrentUser,
) -> UserRolesEnum:
    pass


def get_all_users(request: Request) -> list[User]:
    return []


def get(db_session: DbSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db_session.scalars(stmt).one_or_none()


def get_by_username(db_session: DbSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db_session.scalars(stmt).one_or_none()


def create(db_session: DbSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump(exclude={"password", "role"}), password=user_in.password)

    # role = UserRolesEnum.student
    # if hasattr(user_in, "role"):
    #     role = user_in.role

    db_session.add(user)
    db_session.commit()
    return user
