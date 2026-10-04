from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class ConversationRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.conversations

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc["created_at"] = now
        doc["updated_at"] = now
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def find_by_id(self, conversation_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(conversation_id, str):
            if not ObjectId.is_valid(conversation_id):
                return None
            conversation_id = ObjectId(conversation_id)
        return await self._collection.find_one({"_id": conversation_id})

    async def find_between(
        self, user_a_id: ObjectId, user_b_id: ObjectId, listing_id: str | None
    ) -> dict[str, Any] | None:
        return await self._collection.find_one(
            {
                "participant_ids": {"$all": [user_a_id, user_b_id]},
                "listing_id": listing_id,
            }
        )

    async def list_for_user(
        self, user_id: ObjectId, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        query = {"participant_ids": user_id}
        total = await self._collection.count_documents(query)
        cursor = (
            self._collection.find(query)
            .sort([("last_message_at", -1), ("created_at", -1)])
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items, total

    async def touch_last_message(self, conversation_id: ObjectId, preview: str, at: datetime) -> None:
        await self._collection.update_one(
            {"_id": conversation_id},
            {"$set": {"last_message_preview": preview, "last_message_at": at, "updated_at": at}},
        )
