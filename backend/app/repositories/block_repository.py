from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class BlockRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.blocks

    async def find(self, blocker_id: ObjectId, blocked_id: ObjectId) -> dict[str, Any] | None:
        return await self._collection.find_one({"blocker_id": blocker_id, "blocked_id": blocked_id})

    async def exists_either_direction(self, user_a: ObjectId, user_b: ObjectId) -> bool:
        count = await self._collection.count_documents(
            {
                "$or": [
                    {"blocker_id": user_a, "blocked_id": user_b},
                    {"blocker_id": user_b, "blocked_id": user_a},
                ]
            }
        )
        return count > 0

    async def create(self, blocker_id: ObjectId, blocked_id: ObjectId) -> dict[str, Any]:
        doc = {"blocker_id": blocker_id, "blocked_id": blocked_id, "created_at": datetime.now(timezone.utc)}
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def delete(self, blocker_id: ObjectId, blocked_id: ObjectId) -> None:
        await self._collection.delete_one({"blocker_id": blocker_id, "blocked_id": blocked_id})

    async def list_by_blocker(self, blocker_id: ObjectId) -> list[dict[str, Any]]:
        cursor = self._collection.find({"blocker_id": blocker_id}).sort("created_at", -1)
        return await cursor.to_list(length=200)
