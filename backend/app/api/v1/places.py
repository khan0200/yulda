from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_db
from app.core.responses import ApiResponse
from app.schemas.place import PlaceCreate, PlacePublic
from app.services.place_service import PlaceService

router = APIRouter(prefix="/places", tags=["places"])


def get_place_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> PlaceService:
    return PlaceService(db)


@router.get("/search", response_model=ApiResponse[list[PlacePublic]])
async def search_places(
    q: str = Query(min_length=1, max_length=150),
    country: str | None = Query(default=None, min_length=2, max_length=2),
    limit: int = Query(default=10, ge=1, le=20),
    service: PlaceService = Depends(get_place_service),
):
    places = await service.search(q, country, limit)
    return ApiResponse(data=[PlacePublic.model_validate(p) for p in places])


@router.post("", response_model=ApiResponse[PlacePublic], status_code=201)
async def learn_place(payload: PlaceCreate, service: PlaceService = Depends(get_place_service)):
    place = await service.learn(payload)
    return ApiResponse(data=PlacePublic.model_validate(place), message="Place saved")
