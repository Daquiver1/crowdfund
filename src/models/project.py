"""Project model."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import Field, FutureDatetime

from src.models.core import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin_,
    IsDeletedModelMixin,
)


class ProjectBase(CoreModel):
    """Base model for Project."""

    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    goal_amount: int = Field(..., ge=0)
    owner_id: UUID
    deadline: FutureDatetime = Field(..., description="Deadline must be a future date")


class ProjectCreate(ProjectBase):
    """Model for creating a Project."""

    pass


class ProjectPublic(ProjectBase, DateTimeModelMixin, IDModelMixin_):
    """Public model for Project."""

    total_contributions: Decimal = Field(default=0, ge=0)
    contributors: list[str] = Field(default_factory=list)


class ProjectInDb(ProjectPublic, IsDeletedModelMixin):
    """Model for Project stored in the Database."""

    pass


class ProjectUpdate(CoreModel):
    """Model for updating a Project."""

    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    goal_amount: Optional[Decimal] = Field(None, ge=0)
    deadline: Optional[datetime] = Field(
        None, description="Deadline must be a future date"
    )
