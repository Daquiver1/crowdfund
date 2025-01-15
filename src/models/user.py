"""User model."""

from pydantic import EmailStr, Field

from src.models.core import (
    CoreModel,
    DateTimeModelMixin,
    IsDeletedModelMixin,
    UserIDModelMixin,
)


class UserBase(CoreModel):
    """User base model"""

    email: EmailStr = Field(..., min_length=2)


class UserCreate(UserBase):
    """User create model"""

    password_hash: str = Field(..., min_length=7)


class UserPublic(UserBase, DateTimeModelMixin, UserIDModelMixin):
    """User Public model"""

    pass


class UserInDb(UserPublic, IsDeletedModelMixin):
    """User in Db model"""

    password_hash: str = Field(..., min_length=7)
