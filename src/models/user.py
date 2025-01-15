"""User model."""

from pydantic import EmailStr, Field, validator

from src.models.core import (
    CoreModel,
    DateTimeModelMixin,
    IsDeletedModelMixin,
    UserIDModelMixin,
)


class UserBase(CoreModel):
    """User base model"""

    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)

    @validator("email", "username", pre=True, always=True)
    def to_lowercase(cls, value: str) -> str:
        """Ensure email and username are stored in lowercase."""
        return value.lower()


class UserCreate(UserBase):
    """User create model"""

    password_hash: str = Field(..., min_length=7)


class UserPublic(UserBase, DateTimeModelMixin, UserIDModelMixin):
    """User Public model"""

    pass


class UserInDb(UserPublic, IsDeletedModelMixin):
    """User in Db model"""

    password_hash: str = Field(..., min_length=7)
