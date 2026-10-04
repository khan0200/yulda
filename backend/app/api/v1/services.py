from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse, PaginatedData
from app.models.service import ServiceCategory
from app.schemas.service import ServicePostCreate, ServicePostPublic, ServicePostUpdate
from app.services.service_service import ServicePostService

router = APIRouter(prefix="/services", tags=["services"])


def get_service_post_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> ServicePostService:
    return ServicePostService(db)


@router.get("/posts", response_model=ApiResponse[PaginatedData[ServicePostPublic]])
async def list_posts(
    category: ServiceCategory | None = None,
    city: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    service: ServicePostService = Depends(get_service_post_service),
):
    items, total = await service.list_posts(
        category=category.value if category else None,
        city=city,
        page=page,
        page_size=page_size,
    )
    return ApiResponse(
        data=PaginatedData(
            items=[ServicePostPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/posts", response_model=ApiResponse[ServicePostPublic], status_code=201)
async def create_post(
    payload: ServicePostCreate,
    user: dict = Depends(get_current_user),
    service: ServicePostService = Depends(get_service_post_service),
):
    post = await service.create_post(user, payload)
    return ApiResponse(data=ServicePostPublic.model_validate(post), message="Service post created")


@router.get("/posts/mine", response_model=ApiResponse[PaginatedData[ServicePostPublic]])
async def list_my_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    user: dict = Depends(get_current_user),
    service: ServicePostService = Depends(get_service_post_service),
):
    items, total = await service.list_my_posts(user, page=page, page_size=page_size)
    return ApiResponse(
        data=PaginatedData(
            items=[ServicePostPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/posts/{service_id}/repost", response_model=ApiResponse[ServicePostPublic])
async def repost_post(
    service_id: str,
    user: dict = Depends(get_current_user),
    service: ServicePostService = Depends(get_service_post_service),
):
    post = await service.repost_post(service_id, user)
    return ApiResponse(data=ServicePostPublic.model_validate(post), message="Service post reposted")


@router.get("/posts/{service_id}", response_model=ApiResponse[ServicePostPublic])
async def get_post(service_id: str, service: ServicePostService = Depends(get_service_post_service)):
    post = await service.get_post(service_id)
    return ApiResponse(data=ServicePostPublic.model_validate(post))


@router.patch("/posts/{service_id}", response_model=ApiResponse[ServicePostPublic])
async def update_post(
    service_id: str,
    payload: ServicePostUpdate,
    user: dict = Depends(get_current_user),
    service: ServicePostService = Depends(get_service_post_service),
):
    post = await service.update_post(service_id, user, payload)
    return ApiResponse(data=ServicePostPublic.model_validate(post), message="Service post updated")


@router.delete("/posts/{service_id}", response_model=ApiResponse[None])
async def delete_post(
    service_id: str,
    user: dict = Depends(get_current_user),
    service: ServicePostService = Depends(get_service_post_service),
):
    await service.delete_post(service_id, user)
    return ApiResponse(data=None, message="Service post deleted")
