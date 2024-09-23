from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from feedbacker.database import Base
from .roles import UserRoles

from feedbacker.config import (
    FEEDBACKER_JWT_SECRET,
    FEEDBACKER_JWT_ALG,
    FEEDBACKER_JWT_EXP,
)


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

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)
    
    @property
    def token(self):
        now = datetime.now(timezone.utc)
        exp = (now + timedelta(seconds=FEEDBACKER_JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "email": self.email,
            "roles": self.get_roles(),
        }
        return jwt.encode(data, key=FEEDBACKER_JWT_SECRET, algorithm=FEEDBACKER_JWT_ALG)

    def get_roles(self):
        """Gets the user's role for a given organization slug."""
        # for o in self.organizations:
        #     if o.organization.slug == organization_slug:
        #         return o.role
        return []
