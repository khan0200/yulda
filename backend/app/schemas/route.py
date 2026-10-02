from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.pyobjectid import PyObjectId
from app.models.route import RoutePostType, RouteStatus
from app.schemas.common import OwnerSummary


class RouteStop(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    country: str = Field(min_length=2, max_length=2)


class RoutePostCreate(BaseModel):
    post_type: RoutePostType
    stops: list[RouteStop] = Field(min_length=2, max_length=20)
    departure_at: datetime
    vehicle_info: str | None = Field(default=None, max_length=150)
    seats: int | None = Field(default=None, ge=0, le=50)
    has_cargo_space: bool = False
    price_note: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=1000)
    contact_phone: str = Field(min_length=1, max_length=32)

    @field_validator("stops")
    @classmethod
    def stops_must_be_distinct_in_sequence(cls, stops: list[RouteStop]) -> list[RouteStop]:
        names = [s.name.strip().lower() for s in stops]
        for i in range(len(names) - 1):
            if names[i] == names[i + 1]:
                raise ValueError("Consecutive stops cannot be identical")
        return stops


class RoutePostUpdate(BaseModel):
    stops: list[RouteStop] | None = Field(default=None, min_length=2, max_length=20)
    departure_at: datetime | None = None
    vehicle_info: str | None = Field(default=None, max_length=150)
    seats: int | None = Field(default=None, ge=0, le=50)
    has_cargo_space: bool | None = None
    price_note: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=1000)
    contact_phone: str | None = Field(default=None, min_length=1, max_length=32)


class RoutePostPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    post_type: RoutePostType
    stops: list[RouteStop]
    departure_at: datetime
    vehicle_info: str | None = None
    seats: int | None = None
    has_cargo_space: bool = False
    price_note: str | None = None
    notes: str | None = None
    contact_phone: str
    status: RouteStatus
    owner: OwnerSummary
    created_at: datetime
    updated_at: datetime


class RouteSearchResult(BaseModel):
    items: list[RoutePostPublic]
    total: int
    page: int
    page_size: int
    has_more: bool
    suggested_other_dates: list[RoutePostPublic] = Field(default_factory=list)
    """Populated only when `items` is empty and from/to city were both given."""


class RepostRequest(BaseModel):
    departure_at: datetime
