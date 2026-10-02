from pydantic import BaseModel, Field


class GeoPoint(BaseModel):
    type: str = Field(default="Point", frozen=True)
    coordinates: tuple[float, float]
    """[longitude, latitude]"""
