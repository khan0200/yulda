from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.pyobjectid import PyObjectId
from app.models.cargo import CargoCategory, CargoPostType, CargoStatus
from app.schemas.common import OwnerSummary
from app.schemas.route import RouteStop


class CargoPostCreate(BaseModel):
    post_type: CargoPostType
    stops: list[RouteStop] = Field(min_length=2, max_length=20)
    departure_at: datetime
    accepted_categories: list[CargoCategory] = Field(default_factory=list)
    rejected_categories: list[CargoCategory] = Field(default_factory=list)
    max_weight_kg: float | None = Field(default=None, ge=0, le=1000)
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


class CargoPostUpdate(BaseModel):
    stops: list[RouteStop] | None = Field(default=None, min_length=2, max_length=20)
    departure_at: datetime | None = None
    accepted_categories: list[CargoCategory] | None = None
    rejected_categories: list[CargoCategory] | None = None
    max_weight_kg: float | None = Field(default=None, ge=0, le=1000)
    price_note: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=1000)
    contact_phone: str | None = Field(default=None, min_length=1, max_length=32)


class CargoPostPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    post_type: CargoPostType
    stops: list[RouteStop]
    departure_at: datetime
    accepted_categories: list[CargoCategory]
    rejected_categories: list[CargoCategory]
    max_weight_kg: float | None = None
    price_note: str | None = None
    notes: str | None = None
    contact_phone: str
    status: CargoStatus
    owner: OwnerSummary
    created_at: datetime
    updated_at: datetime


class CargoSearchResult(BaseModel):
    items: list[CargoPostPublic]
    total: int
    page: int
    page_size: int
    has_more: bool
    suggested_other_dates: list[CargoPostPublic] = Field(default_factory=list)


class CargoRepostRequest(BaseModel):
    departure_at: datetime
