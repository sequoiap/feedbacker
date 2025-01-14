from typing import Optional
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import ForeignKey, Table, Integer, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy

from feedbacker.database import Base
from feedbacker.config import (
    FEEDBACKER_JWT_SECRET,
    FEEDBACKER_JWT_ALG,
    FEEDBACKER_JWT_EXP,
)

from .roles import UserRolesEnum

class User(Base):
    """User model.
    
    Passwords are hashed using bcrypt.

    Args:
        username: The user's username.
        password: The user's password.
        email: The user's email address.
        firstname: The user's first name.
        lastname: The user's last name.
        created_at: The date and time the user was created (default now).
        updated_at: The date and time the user was last updated (default now).
        last_login_time: The date and time the user last logged.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(index=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(index=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
    last_login_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    role: Mapped[list["Role"]] = relationship(secondary=lambda: user_roles_table)

    roles: AssociationProxy[list[str]] = association_proxy("role", "role")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)
    
    def create_token(self):
        now = datetime.now(timezone.utc)
        exp = (now + timedelta(seconds=FEEDBACKER_JWT_EXP)).timestamp()
        data = {
            "sub": self.username,
            "exp": exp,
            "email": self.email,
            # "roles": self.get_roles(),
            "roles": [role for role in self.roles],
        }
        return jwt.encode(data, key=FEEDBACKER_JWT_SECRET, algorithm=FEEDBACKER_JWT_ALG)
    
    def check_permissions(self, required_permissions: list[str]) -> bool:
        for permission in required_permissions:
            if permission not in self.roles:
                return False
        return True
    
    def has_any_permission(self, permissions: list[str]) -> bool:
        for permission in permissions:
            if permission in self.roles:
                return True
        return False

    # def get_roles(self) -> list[str]:
    #     """Gets the user's role for a given organization slug."""
    #     return [role.role for role in self.roles]


class Role(Base):
    """User roles model."""
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    role: Mapped[str] = mapped_column(index=True)

    def __init__(self, role: str):
        if role not in UserRolesEnum:
            raise ValueError(f"Invalid role '{role}'.")
        self.role = role


user_roles_table: Table = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)
