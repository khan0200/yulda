from __future__ import annotations

from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationPublic
from app.websocket.manager import manager


class NotificationService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = NotificationRepository(db)

    async def create_and_push(
        self, user_id: ObjectId, type_: str, title: str, body: str, link: str | None = None
    ) -> dict[str, Any]:
        doc = {"user_id": user_id, "type": type_, "title": title, "body": body, "link": link, "is_read": False}
        notification = await self._repo.create(doc)
        public = NotificationPublic.model_validate(notification).model_dump(mode="json")
        await manager.send_to_user(str(user_id), {"event": "notification", "notification": public})
        return notification

    async def list_my_notifications(
        self, user: dict[str, Any], page: int, page_size: int
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list_for_user(user["_id"], page=page, page_size=page_size)

    async def unread_count(self, user: dict[str, Any]) -> int:
        return await self._repo.count_unread(user["_id"])

    async def mark_read(self, notification_id: str, user: dict[str, Any]) -> dict[str, Any]:
        notification = await self._repo.find_by_id(notification_id)
        if not notification or notification["user_id"] != user["_id"]:
            raise NotFoundError("Notification not found")
        await self._repo.mark_read(notification["_id"], user["_id"])
        notification["is_read"] = True
        return notification

    async def mark_all_read(self, user: dict[str, Any]) -> None:
        await self._repo.mark_all_read(user["_id"])
