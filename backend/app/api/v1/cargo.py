from datetime import datetime

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse
from app.models.cargo import CargoPostType
from app.schemas.cargo import (
    CargoPostCreate,
    CargoPostPublic,
    CargoPostUpdate,
    CargoRepostRequest,
    CargoSearchResult,
)
from app.services.cargo_service import CargoService

router = APIRouter(prefix="/cargo", tags=["cargo"])


def get_cargo_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> CargoService:
    return CargoService(db)


@router.get("/search", response_model=ApiResponse[CargoSearchResult])
async def search_cargo(
    post_type: CargoPostType | None = None,
    from_city: str | None = None,
    to_city: str | None = None,
    date: datetime | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    service: CargoService = Depends(get_cargo_service),
):
    items, total = await service.search(
        post_type=post_type.value if post_type else None,
        from_city=from_city,
        to_city=to_city,
        date=date,
        page=page,
        page_size=page_size,
    )

    suggested: list[dict] = []
    if not items and date and from_city and to_city:
        suggested = await service.search_nearby_dates(
            post_type=post_type.value if post_type else None,
            from_city=from_city,
            to_city=to_city,
            center_date=date,
            window_days=5,
        )

    return ApiResponse(
        data=CargoSearchResult(
            items=[CargoPostPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
            suggested_other_dates=[CargoPostPublic.model_validate(item) for item in suggested],
        )
    )


@router.post("", response_model=ApiResponse[CargoPostPublic], status_code=201)
async def create_cargo_post(
    payload: CargoPostCreate,
    user: dict = Depends(get_current_user),
    service: CargoService = Depends(get_cargo_service),
):
    post = await service.create_post(user, payload)
    return ApiResponse(data=CargoPostPublic.model_validate(post), message="Post created")


@router.get("/{post_id}", response_model=ApiResponse[CargoPostPublic])
async def get_cargo_post(post_id: str, service: CargoService = Depends(get_cargo_service)):
    post = await service.get_post(post_id)
    return ApiResponse(data=CargoPostPublic.model_validate(post))


@router.patch("/{post_id}", response_model=ApiResponse[CargoPostPublic])
async def update_cargo_post(
    post_id: str,
    payload: CargoPostUpdate,
    user: dict = Depends(get_current_user),
    service: CargoService = Depends(get_cargo_service),
):
    post = await service.update_post(post_id, user, payload)
    return ApiResponse(data=CargoPostPublic.model_validate(post), message="Post updated")


@router.post("/{post_id}/deactivate", response_model=ApiResponse[CargoPostPublic])
async def deactivate_cargo_post(
    post_id: str,
    user: dict = Depends(get_current_user),
    service: CargoService = Depends(get_cargo_service),
):
    post = await service.deactivate_post(post_id, user)
    return ApiResponse(data=CargoPostPublic.model_validate(post), message="Post deactivated")


@router.post("/{post_id}/repost", response_model=ApiResponse[CargoPostPublic])
async def repost_cargo_post(
    post_id: str,
    payload: CargoRepostRequest,
    user: dict = Depends(get_current_user),
    service: CargoService = Depends(get_cargo_service),
):
    post = await service.repost(post_id, user, payload.departure_at)
    return ApiResponse(data=CargoPostPublic.model_validate(post), message="Post reactivated")


@router.delete("/{post_id}", response_model=ApiResponse[None])
async def delete_cargo_post(
    post_id: str,
    user: dict = Depends(get_current_user),
    service: CargoService = Depends(get_cargo_service),
):
    await service.delete_post(post_id, user)
    return ApiResponse(data=None, message="Post deleted")
