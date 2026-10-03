from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.service import ServiceCategory, ServiceStatus
from app.schemas.common import GeoPoint, OwnerSummary


class ServicePostCreate(BaseModel):
    category: ServiceCategory
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=5000)
    price_note: str | None = Field(default=None, max_length=200)
    city: str | None = Field(default=None, max_length=100)
    location: GeoPoint | None = None
    photos: list[str] = Field(default_factory=list, max_length=9)
    contact_value: str = Field(min_length=1, max_length=200)


class ServicePostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    price_note: str | None = Field(default=None, max_length=200)
    photos: list[str] | None = Field(default=None, max_length=9)
    status: ServiceStatus | None = None


class ServicePostPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    category: ServiceCategory
    title: str
    description: str
    price_note: str | None = None
    city: str | None = None
    location: GeoPoint | None = None
    photos: list[str]
    contact_value: str
    status: ServiceStatus
    owner: OwnerSummary
    like_count: int = 0
    created_at: datetime
    updated_at: datetime
