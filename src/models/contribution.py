"""Contribution model."""

from decimal import Decimal
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
    amount: Decimal = Field(..., ge=0.01, description="Minimum contribution is 0.01")


class ContributionCreate(ContributionBase):
    """Model for creating a Contribution."""

    pass


class ContributionPublic(ContributionBase, DateTimeModelMixin, IDModelMixin_):
    """Public model for Contribution."""

    pass


class ContributionInDb(ContributionPublic, IsDeletedModelMixin):
    """Model for Contribution stored in the Database."""

    pass


class ContributionUpdate(CoreModel):
    """Model for updating a Contribution."""

    amount: Optional[Decimal] = Field(
        None, ge=0.01, description="Minimum contribution is 0.01"
    )
