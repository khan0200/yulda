from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse
from app.models.favorite import FavoriteTargetType
from app.services.favorite_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["favorites"])


class ToggleFavoriteResponse(BaseModel):
    is_favorited: bool
    like_count: int


def get_favorite_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> FavoriteService:
    return FavoriteService(db)


@router.post("/{target_type}/{target_id}/toggle", response_model=ApiResponse[ToggleFavoriteResponse])
async def toggle_favorite(
    target_type: FavoriteTargetType,
    target_id: str,
    user: dict = Depends(get_current_user),
    service: FavoriteService = Depends(get_favorite_service),
):
    result = await service.toggle(user["_id"], target_type.value, target_id)
    return ApiResponse(data=ToggleFavoriteResponse(**result))


@router.get("/{target_type}/mine", response_model=ApiResponse[list[str]])
async def list_my_favorites(
    target_type: FavoriteTargetType,
    user: dict = Depends(get_current_user),
    service: FavoriteService = Depends(get_favorite_service),
):
    ids = await service.list_favorited_ids(user["_id"], target_type.value)
    return ApiResponse(data=sorted(ids))
