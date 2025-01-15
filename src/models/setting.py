"""Settings model."""

from typing import Optional

from pydantic import BaseModel, Field

from src.models.core import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin_,
    IsDeletedModelMixin,
)


class SettingsBase(BaseModel):
    """Settings base model."""

    key: str = Field(...)
    value: str = Field(...)


class SettingsCreate(SettingsBase):
    """Settings create model."""

    pass


class SettingsPublic(SettingsBase, DateTimeModelMixin, IDModelMixin_):
    """Settings public model."""

    pass


class SettingsInDb(SettingsPublic, IsDeletedModelMixin):
    """Settings in db model."""

    pass


class SettingsUpdate(CoreModel):
    """Settings update model."""

    key: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
