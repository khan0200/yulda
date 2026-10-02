from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.place import PlaceCountry, PlaceSource


class PlacePublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    name: str
    country: PlaceCountry
    admin1: str | None = None
    lat: float | None = None
    lon: float | None = None
    source: PlaceSource
    usage_count: int = 0


class PlaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    country: PlaceCountry
