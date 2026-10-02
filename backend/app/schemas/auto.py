from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.auto import AutoListingStatus, AutoListingType, FuelType, TransmissionType
from app.schemas.common import GeoPoint, OwnerSummary


class AutoListingCreate(BaseModel):
    listing_type: AutoListingType
    make: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1980, le=2100)
    mileage_km: int = Field(ge=0, le=2_000_000)
    fuel_type: FuelType
    transmission: TransmissionType
    price: int = Field(ge=0, le=10_000_000_000)
    rental_price_per_day: int | None = Field(default=None, ge=0, le=10_000_000_000)
    description: str = Field(min_length=1, max_length=5000)
    photos: list[str] = Field(default_factory=list, max_length=9)
    city: str | None = Field(default=None, max_length=100)
    contact_value: str = Field(min_length=1, max_length=200)
    location: GeoPoint | None = None


class AutoListingUpdate(BaseModel):
    price: int | None = Field(default=None, ge=0, le=10_000_000_000)
    rental_price_per_day: int | None = Field(default=None, ge=0, le=10_000_000_000)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    mileage_km: int | None = Field(default=None, ge=0, le=2_000_000)
    photos: list[str] | None = Field(default=None, max_length=9)
    status: AutoListingStatus | None = None


class AutoListingPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    listing_type: AutoListingType
    make: str
    model: str
    year: int
    mileage_km: int
    fuel_type: FuelType
    transmission: TransmissionType
    price: int
    rental_price_per_day: int | None = None
    description: str
    photos: list[str]
    city: str | None = None
    location: GeoPoint | None = None
    contact_value: str
    status: AutoListingStatus
    owner: OwnerSummary
    created_at: datetime
    updated_at: datetime
