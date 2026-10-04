from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class MessageRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.messages

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        doc["created_at"] = datetime.now(timezone.utc)
        doc.setdefault("read_at", None)
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def list_for_conversation(
        self, conversation_id: ObjectId, page: int = 1, page_size: int = 50
    ) -> tuple[list[dict[str, Any]], int]:
        query = {"conversation_id": conversation_id}
        total = await self._collection.count_documents(query)
        cursor = (
            self._collection.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        items.reverse()
        return items, total

    async def mark_read(self, conversation_id: ObjectId, reader_id: ObjectId) -> None:
        await self._collection.update_many(
            {"conversation_id": conversation_id, "sender_id": {"$ne": reader_id}, "read_at": None},
            {"$set": {"read_at": datetime.now(timezone.utc)}},
        )

    async def count_unread(self, conversation_id: ObjectId, reader_id: ObjectId) -> int:
        return await self._collection.count_documents(
            {"conversation_id": conversation_id, "sender_id": {"$ne": reader_id}, "read_at": None}
        )
