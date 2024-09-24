from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

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
    last_login_time: Mapped[datetime] = mapped_column(nullable=True)

    roles = relationship("UserRoles", back_populates="user")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)
    
    def create_token(self):
        now = datetime.now(timezone.utc)
        exp = (now + timedelta(seconds=FEEDBACKER_JWT_EXP)).timestamp()
        data = {
            "sub": self.username,
            "exp": exp,
            "email": self.email,
            "roles": self.get_roles(),
        }
        return jwt.encode(data, key=FEEDBACKER_JWT_SECRET, algorithm=FEEDBACKER_JWT_ALG)

    def get_roles(self):
        """Gets the user's role for a given organization slug."""
        return [role.role for role in self.roles]


class UserRoles(Base):
    """User roles model."""
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(index=True)

    user = relationship("User", back_populates="roles")

    def __init__(self, user_id: int, role: str):
        if role not in UserRolesEnum:
            raise ValueError(f"Invalid role '{role}'.")
