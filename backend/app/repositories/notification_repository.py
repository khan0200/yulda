from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class NotificationRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.notifications

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        doc["created_at"] = datetime.now(timezone.utc)
        doc.setdefault("is_read", False)
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def find_by_id(self, notification_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(notification_id, str):
            if not ObjectId.is_valid(notification_id):
                return None
            notification_id = ObjectId(notification_id)
        return await self._collection.find_one({"_id": notification_id})

    async def list_for_user(
        self, user_id: ObjectId, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        query = {"user_id": user_id}
        total = await self._collection.count_documents(query)
        cursor = (
            self._collection.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items, total

    async def count_unread(self, user_id: ObjectId) -> int:
        return await self._collection.count_documents({"user_id": user_id, "is_read": False})

    async def mark_read(self, notification_id: ObjectId, user_id: ObjectId) -> None:
        await self._collection.update_one(
            {"_id": notification_id, "user_id": user_id}, {"$set": {"is_read": True}}
        )

    async def mark_all_read(self, user_id: ObjectId) -> None:
        await self._collection.update_many({"user_id": user_id, "is_read": False}, {"$set": {"is_read": True}})
