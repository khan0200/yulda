from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_db, require_roles
from app.core.responses import ApiResponse, PaginatedData
from app.models.user import UserRole
from app.schemas.user import UserPublic
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


def get_admin_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> AdminService:
    return AdminService(db)


@router.get("/users", response_model=ApiResponse[PaginatedData[UserPublic]])
async def list_users(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    _admin: dict = Depends(require_roles(UserRole.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    items, total = await service.list_users(search, page=page, page_size=page_size)
    return ApiResponse(
        data=PaginatedData(
            items=[UserPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/users/{user_id}/ban", response_model=ApiResponse[UserPublic])
async def ban_user(
    user_id: str,
    admin: dict = Depends(require_roles(UserRole.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    user = await service.set_user_banned(admin, user_id, True)
    return ApiResponse(data=UserPublic.model_validate(user), message="User banned")


@router.post("/users/{user_id}/unban", response_model=ApiResponse[UserPublic])
async def unban_user(
    user_id: str,
    admin: dict = Depends(require_roles(UserRole.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    user = await service.set_user_banned(admin, user_id, False)
    return ApiResponse(data=UserPublic.model_validate(user), message="User unbanned")


@router.delete("/content/{target_type}/{content_id}", response_model=ApiResponse[None])
async def remove_content(
    target_type: str,
    content_id: str,
    _admin: dict = Depends(require_roles(UserRole.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    await service.remove_content(target_type, content_id)
    return ApiResponse(data=None, message="Content removed")
