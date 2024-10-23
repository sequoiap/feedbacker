from typing import Annotated, Optional, Dict

import jwt
from fastapi import Depends, HTTPException, Security, status, WebSocket, Cookie, WebSocketException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
    OAuth2,
)
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.requests import Request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from feedbacker.auth.roles import UserRolesEnum
from feedbacker.auth.schemas import UserCreate
from feedbacker.database import DbSession
from feedbacker.config import (
    FEEDBACKER_JWT_SECRET,
    FEEDBACKER_JWT_ALG,
    AUTH_COOKIE_NAME,
    REFRESH_COOKIE_NAME,
)

from .models import User


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(AUTH_COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        "admin": "Admin users",
        "dev": "Developer users",
        "instructor": "Instructor users",
        "student": "Student users",
    }
)


def authenticate_user(db_session: DbSession, username: str, password: str) -> User | bool:
    user = get_by_username(db_session, username)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user


def decode_token(db_session: DbSession, token: str) -> User:
    """Decode a JWT token and return the user.
    
    Args:
        db_session: The database session.
        token: The JWT auth token.

    Returns:
        The user.

    Raises:
        HTTPException: If the token is invalid.
    """
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


async def get_current_user(db_session: DbSession, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    return decode_token(db_session, token)


CurrentUser = Annotated[User, Depends(get_current_user)]


# def get_current_role(
#     request: Request,
#     current_user: CurrentUser,
# ) -> UserRolesEnum:
#     pass


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


class AuthorizedAPIUser:
    """Check if a user has the required permissions.

    Based on https://dev.to/moadennagi/role-based-access-control-using-fastapi-h59.
    
    Examples:
        >>> @app.get('/items')
        ... def items(
        ...     authorize: bool = Depends(PermissionChecker(required_permissions=['items:read',]))
        ... ):
        ...     return 'items'
    """
    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: CurrentUser) -> User:
        if user.check_permissions(self.required_permissions):
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Permission denied (insufficient permissions).'
        )


async def ws_get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
):
    if session is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session
