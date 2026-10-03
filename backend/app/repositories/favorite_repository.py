from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class FavoriteRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.favorites

    async def find(self, user_id: ObjectId, target_type: str, target_id: ObjectId) -> dict[str, Any] | None:
        return await self._collection.find_one(
            {"user_id": user_id, "target_type": target_type, "target_id": target_id}
        )

    async def add(self, user_id: ObjectId, target_type: str, target_id: ObjectId) -> None:
        existing = await self.find(user_id, target_type, target_id)
        if existing:
            return
        await self._collection.insert_one(
            {
                "user_id": user_id,
                "target_type": target_type,
                "target_id": target_id,
                "created_at": datetime.now(timezone.utc),
            }
        )

    async def remove(self, user_id: ObjectId, target_type: str, target_id: ObjectId) -> None:
        await self._collection.delete_one(
            {"user_id": user_id, "target_type": target_type, "target_id": target_id}
        )

    async def list_target_ids_for_user(self, user_id: ObjectId, target_type: str) -> set[str]:
        cursor = self._collection.find({"user_id": user_id, "target_type": target_type}, {"target_id": 1})
        docs = await cursor.to_list(length=None)
        return {str(doc["target_id"]) for doc in docs}
