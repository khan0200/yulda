from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse, PaginatedData
from app.schemas.notification import NotificationPublic
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


class UnreadCountResponse(BaseModel):
    unread_count: int


def get_notification_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> NotificationService:
    return NotificationService(db)


@router.get("", response_model=ApiResponse[PaginatedData[NotificationPublic]])
async def list_my_notifications(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    user: dict = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
):
    items, total = await service.list_my_notifications(user, page=page, page_size=page_size)
    return ApiResponse(
        data=PaginatedData(
            items=[NotificationPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.get("/unread-count", response_model=ApiResponse[UnreadCountResponse])
async def unread_count(
    user: dict = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
):
    count = await service.unread_count(user)
    return ApiResponse(data=UnreadCountResponse(unread_count=count))


@router.post("/{notification_id}/read", response_model=ApiResponse[NotificationPublic])
async def mark_notification_read(
    notification_id: str,
    user: dict = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
):
    notification = await service.mark_read(notification_id, user)
    return ApiResponse(data=NotificationPublic.model_validate(notification), message="Marked as read")


@router.post("/read-all", response_model=ApiResponse[None])
async def mark_all_notifications_read(
    user: dict = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
):
    await service.mark_all_read(user)
    return ApiResponse(data=None, message="All notifications marked as read")
