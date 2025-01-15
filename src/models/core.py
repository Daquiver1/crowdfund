"""Core data that exist in all Models."""

# Standard library imports
from datetime import datetime, timezone
from typing import Type
from uuid import UUID

# Third party imports
from pydantic import BaseModel, Field

from src.db.repositories.base import BaseRepository


class CoreModel(BaseModel):
    """Any common logic to be shared by all models."""

    class Config:
        """Configurations for the class."""

        from_attributes = True
        validate_assignment = True
        extra = "forbid"
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class IDModelMixin(BaseModel):
    """ID data."""

    id: int


def datetime_now() -> datetime:
    """Get current datetime."""
    return datetime.now(timezone.utc)


class DateTimeModelMixin(CoreModel):
    """Datetime model dates."""

    created_at: datetime = Field(default_factory=datetime_now)
    updated_at: datetime = Field(default_factory=datetime_now)


class IDModelMixin_(BaseModel):
    """ID data."""

    id: UUID


class UserIDModelMixin(BaseModel):
    """User ID data."""

    user_id: UUID


class IsDeletedModelMixin(BaseModel):
    """Is deleted data."""

    is_deleted: bool = False


class EntityValidator(BaseModel):
    """Entity validator."""

    field_name: str
    repo_type: Type[BaseRepository]
    get_method: str
