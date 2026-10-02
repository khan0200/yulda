from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId


class GeoPoint(BaseModel):
    type: str = Field(default="Point", frozen=True)
    coordinates: tuple[float, float]
    """[longitude, latitude]"""


class OwnerSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    name: str
    avatar: str | None = None
