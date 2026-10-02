from datetime import datetime

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse
from app.models.route import RoutePostType
from app.schemas.route import (
    RepostRequest,
    RoutePostCreate,
    RoutePostPublic,
    RoutePostUpdate,
    RouteSearchResult,
)
from app.services.route_service import RouteService

router = APIRouter(prefix="/routes", tags=["routes"])


def get_route_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> RouteService:
    return RouteService(db)


@router.get("/search", response_model=ApiResponse[RouteSearchResult])
async def search_routes(
    post_type: RoutePostType | None = None,
    from_city: str | None = None,
    to_city: str | None = None,
    date: datetime | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    service: RouteService = Depends(get_route_service),
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
        data=RouteSearchResult(
            items=[RoutePostPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
            suggested_other_dates=[RoutePostPublic.model_validate(item) for item in suggested],
        )
    )


@router.post("", response_model=ApiResponse[RoutePostPublic], status_code=201)
async def create_route_post(
    payload: RoutePostCreate,
    user: dict = Depends(get_current_user),
    service: RouteService = Depends(get_route_service),
):
    post = await service.create_post(user, payload)
    return ApiResponse(data=RoutePostPublic.model_validate(post), message="Post created")


@router.get("/{post_id}", response_model=ApiResponse[RoutePostPublic])
async def get_route_post(post_id: str, service: RouteService = Depends(get_route_service)):
    post = await service.get_post(post_id)
    return ApiResponse(data=RoutePostPublic.model_validate(post))


@router.patch("/{post_id}", response_model=ApiResponse[RoutePostPublic])
async def update_route_post(
    post_id: str,
    payload: RoutePostUpdate,
    user: dict = Depends(get_current_user),
    service: RouteService = Depends(get_route_service),
):
    post = await service.update_post(post_id, user, payload)
    return ApiResponse(data=RoutePostPublic.model_validate(post), message="Post updated")


@router.post("/{post_id}/deactivate", response_model=ApiResponse[RoutePostPublic])
async def deactivate_route_post(
    post_id: str,
    user: dict = Depends(get_current_user),
    service: RouteService = Depends(get_route_service),
):
    post = await service.deactivate_post(post_id, user)
    return ApiResponse(data=RoutePostPublic.model_validate(post), message="Post deactivated")


@router.post("/{post_id}/repost", response_model=ApiResponse[RoutePostPublic])
async def repost_route_post(
    post_id: str,
    payload: RepostRequest,
    user: dict = Depends(get_current_user),
    service: RouteService = Depends(get_route_service),
):
    post = await service.repost(post_id, user, payload.departure_at)
    return ApiResponse(data=RoutePostPublic.model_validate(post), message="Post reactivated")


@router.delete("/{post_id}", response_model=ApiResponse[None])
async def delete_route_post(
    post_id: str,
    user: dict = Depends(get_current_user),
    service: RouteService = Depends(get_route_service),
):
    await service.delete_post(post_id, user)
    return ApiResponse(data=None, message="Post deleted")
