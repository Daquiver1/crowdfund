"""Profile model."""

from typing import Optional

from pydantic import EmailStr, Field

from src.models.core import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin_,
    IsDeletedModelMixin,
    UserIDModelMixin,
)


class ProfileBase(CoreModel):
    """Profile base model"""

    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=2)


class ProfileCreate(ProfileBase):
    """Profile create model"""

    pass


class ProfilePublic(ProfileBase, DateTimeModelMixin, IDModelMixin_, UserIDModelMixin):
    """Profile Public model"""

    pass


class ProfileInDb(ProfilePublic, IsDeletedModelMixin):
    """Profile in Db model"""

    pass


class ProfileUpdate(CoreModel):
    """Profile update model"""

    first_name: Optional[str] = Field(None, min_length=2)
    last_name: Optional[str] = Field(None, min_length=2)
    username: Optional[str] = Field(None, min_length=3)
