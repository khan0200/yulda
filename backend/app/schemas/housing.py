from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.housing import HousingAmenity, HousingDirection, HousingStatus, HousingType
from app.schemas.common import GeoPoint, OwnerSummary


class HousingCreate(BaseModel):
    housing_type: HousingType
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=5000)
    deposit: int = Field(ge=0, le=10_000_000_000)
    monthly_rent: int = Field(ge=0, le=10_000_000_000)
    maintenance_fee: int = Field(default=0, ge=0, le=10_000_000_000)
    amenities: list[HousingAmenity] = Field(default_factory=list)
    move_in_date: date | None = None
    photos: list[str] = Field(default_factory=list, max_length=9)
    city: str | None = Field(default=None, max_length=100)
    metro_station: str | None = Field(default=None, max_length=100)
    contact_value: str = Field(min_length=1, max_length=200)
    location: GeoPoint | None = None
    area_m2: float | None = Field(default=None, ge=0, le=100_000)
    room_count: int | None = Field(default=None, ge=0, le=50)
    floor: int | None = Field(default=None, ge=-5, le=200)
    total_floors: int | None = Field(default=None, ge=1, le=200)
    building_year: int | None = Field(default=None, ge=1900, le=2100)
    direction: HousingDirection | None = None


class HousingUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    deposit: int | None = Field(default=None, ge=0, le=10_000_000_000)
    monthly_rent: int | None = Field(default=None, ge=0, le=10_000_000_000)
    maintenance_fee: int | None = Field(default=None, ge=0, le=10_000_000_000)
    amenities: list[HousingAmenity] | None = None
    photos: list[str] | None = Field(default=None, max_length=9)
    status: HousingStatus | None = None
    area_m2: float | None = Field(default=None, ge=0, le=100_000)
    room_count: int | None = Field(default=None, ge=0, le=50)
    floor: int | None = Field(default=None, ge=-5, le=200)
    total_floors: int | None = Field(default=None, ge=1, le=200)
    building_year: int | None = Field(default=None, ge=1900, le=2100)
    direction: HousingDirection | None = None


class HousingPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    housing_type: HousingType
    title: str
    description: str
    deposit: int
    monthly_rent: int
    maintenance_fee: int
    amenities: list[HousingAmenity]
    move_in_date: date | None = None
    photos: list[str]
    city: str | None = None
    metro_station: str | None = None
    location: GeoPoint | None = None
    contact_value: str
    status: HousingStatus
    owner: OwnerSummary
    created_at: datetime
    updated_at: datetime
    area_m2: float | None = None
    room_count: int | None = None
    floor: int | None = None
    total_floors: int | None = None
    building_year: int | None = None
    direction: HousingDirection | None = None
