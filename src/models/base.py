"""Core data that exist in all Models."""

# Standard library imports
from datetime import datetime
from typing import Optional
from uuid import UUID

# Third party imports
from pydantic import BaseModel, field_validator


class CoreModel(BaseModel):
    """Any common logic to be shared by all models."""

    class Config:
        """Pydantic config."""

        # orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class IDModelMixin(BaseModel):
    """ID data."""

    id: int


class DateTimeModelMixin(CoreModel):
    """Datetime model dates."""

    created_at: Optional[datetime]
    updated_at: Optional[datetime] = datetime.now()


class IDModelMixin_(BaseModel):
    """ID data."""

    id: UUID


class UserIDModelMixin(BaseModel):
    """ID data."""

    user_id: UUID


class IsDeletedModelMixin(BaseModel):
    """Is deleted data."""

    is_deleted: bool = False


class UpdatedAtModelMixin(BaseModel):
    """Updated at model data."""

    updated_at: Optional[datetime] = datetime.now()

    @field_validator("updated_at")
    def default_datetime(cls, value: datetime) -> datetime:
        """Validate both created_at and update_at data."""
        return datetime.now()

    class Config:
        """Config for datetime model mixin."""

        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
