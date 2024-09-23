from typing import Annotated

from fastapi import Depends
from starlette.requests import Request

from feedbacker.auth.roles import UserRoles

from .models import User


def get_current_user(request: Request) -> User:
    pass


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_role(
    request: Request,
    current_user: CurrentUser,
) -> UserRoles:
    pass
