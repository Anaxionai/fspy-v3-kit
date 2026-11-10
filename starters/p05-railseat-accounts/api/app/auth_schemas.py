"""Request and response models for accounts (P5 add-on, ready to use).

The routes in `app/routers/auth.py` and `app/routers/admin.py` use them.
No response model has a password or a password hash in it.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

RoleName = Literal["passenger", "agent", "admin"]


class SignupIn(BaseModel):
    """POST /auth/signup. Any other field, such as a role, is ignored."""

    email: EmailStr
    password: str = Field(min_length=10, max_length=128)


class UserOut(BaseModel):
    """What the API shows about a user."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: RoleName

    @field_validator("role", mode="before")
    @classmethod
    def role_name(cls, value: object) -> object:
        # User.role is a Role row; the API sends only its name.
        return getattr(value, "name", value)


class TokenIn(BaseModel):
    """POST /auth/verify: the token from the emailed link."""

    token: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class LoginOut(BaseModel):
    """The reply of POST /auth/login and POST /auth/refresh."""

    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ForgotIn(BaseModel):
    email: EmailStr


class ResetIn(BaseModel):
    token: str
    password: str = Field(min_length=10, max_length=128)


class RoleIn(BaseModel):
    """PATCH /admin/users/{user_id}/role."""

    role: RoleName
