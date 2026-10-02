from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.marketplace import ContactMethod, ListingCategory, ListingCondition, ListingStatus
from app.schemas.common import GeoPoint, OwnerSummary


class ListingCreate(BaseModel):
    category: ListingCategory
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=5000)
    price: int = Field(ge=0, le=10_000_000_000)
    condition: ListingCondition
    photos: list[str] = Field(default_factory=list, max_length=9)
    city: str | None = Field(default=None, max_length=100)
    contact_method: ContactMethod
    contact_value: str = Field(min_length=1, max_length=200)
    location: GeoPoint | None = None


class ListingUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    price: int | None = Field(default=None, ge=0, le=10_000_000_000)
    condition: ListingCondition | None = None
    photos: list[str] | None = Field(default=None, max_length=9)
    status: ListingStatus | None = None


class ListingPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    category: ListingCategory
    title: str
    description: str
    price: int
    condition: ListingCondition
    photos: list[str]
    city: str | None = None
    location: GeoPoint | None = None
    contact_method: ContactMethod
    contact_value: str
    status: ListingStatus
    seller: OwnerSummary
    created_at: datetime
    updated_at: datetime
