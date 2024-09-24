from typing import List, Optional

import bcrypt
from pydantic import field_validator, Field
from pydantic.networks import EmailStr

from feedbacker.models import FeedbackerBase, Pagination


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class UserBase(FeedbackerBase):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def email_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string and must be a email")
        return v


class UserLogin(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v


# class UserRegister(UserLogin):
#     password: str = Field(validate_default=True)

#     @field_validator("password")
#     @classmethod
#     def password_required(cls, v):
#         password = v
#         return hash_password(password)


class UserLoginResponse(FeedbackerBase):
    token: Optional[str] = Field(None, nullable=True)


class UserRead(UserBase):
    id: int
    username: str
    firstname: str
    lastname: str
    roles: list[str] = Field([])


class UserUpdate(FeedbackerBase):
    id: int
    username: Optional[str] = Field(None, nullable=True)
    password: Optional[str] = Field(None, nullable=True, validate_default=True)
    roles: Optional[str] = Field(None, nullable=True)

    @field_validator("password")
    @classmethod
    def hash(cls, v):
        return hash_password(str(v))


class UserCreate(FeedbackerBase):
    email: EmailStr
    username: str
    password: str = Field(validate_default=True)
    firstname: str
    lastname: str
    role: list[str] = []

    @field_validator("password")
    @classmethod
    def hash(cls, v):
        return hash_password(str(v))


# class UserRegisterResponse(FeedbackerBase):
#     token: Optional[str] = Field(None, nullable=True)


class UserPagination(Pagination):
    items: List[UserRead] = []


class Token(FeedbackerBase):
    access_token: str
    token_type: str


class TokenData(FeedbackerBase):
    username: str | None = None
