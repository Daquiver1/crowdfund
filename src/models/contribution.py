"""Contribution model."""

from typing import Optional
from uuid import UUID

from pydantic import Field

from src.models.core import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin_,
    IsDeletedModelMixin,
)


class ContributionBase(CoreModel):
    """Base model for Contribution."""

    contributor_id: UUID
    amount: int = Field(..., ge=1, description="Minimum contribution is 1")


class ContributionCreate(ContributionBase):
    """Model for creating a Contribution."""

    pass


class ContributionPublic(ContributionBase, DateTimeModelMixin, IDModelMixin_):
    """Public model for Contribution."""

    project_id: UUID


class ContributionInDb(ContributionPublic, IsDeletedModelMixin):
    """Model for Contribution stored in the Database."""

    pass


class ContributionUpdate(CoreModel):
    """Model for updating a Contribution."""

    amount: Optional[int] = Field(None, ge=1, description="Minimum contribution is 1")
