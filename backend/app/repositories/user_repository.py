from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.users

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        return await self._collection.find_one({"email": email.lower()})

    async def find_by_id(self, user_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(user_id, str):
            if not ObjectId.is_valid(user_id):
                return None
            user_id = ObjectId(user_id)
        return await self._collection.find_one({"_id": user_id})

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc["created_at"] = now
        doc["updated_at"] = now
        doc["email"] = doc["email"].lower()
        if doc.get("phone") is None:
            doc.pop("phone", None)
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def update(self, user_id: ObjectId, updates: dict[str, Any]) -> dict[str, Any] | None:
        updates["updated_at"] = datetime.now(timezone.utc)
        await self._collection.update_one({"_id": user_id}, {"$set": updates})
        return await self.find_by_id(user_id)

    async def set_password_hash(self, user_id: ObjectId, password_hash: str) -> None:
        await self._collection.update_one(
            {"_id": user_id},
            {"$set": {"password_hash": password_hash, "updated_at": datetime.now(timezone.utc)}},
        )

    async def delete(self, user_id: ObjectId) -> None:
        await self._collection.delete_one({"_id": user_id})

    async def list(
        self, page: int = 1, page_size: int = 20, search: str | None = None
    ) -> tuple[list[dict[str, Any]], int]:
        query: dict[str, Any] = {}
        if search:
            pattern = re.compile(re.escape(search), re.IGNORECASE)
            query["$or"] = [{"name": pattern}, {"email": pattern}]
        total = await self._collection.count_documents(query)
        cursor = (
            self._collection.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items, total

    async def set_banned(self, user_id: ObjectId, banned: bool) -> dict[str, Any] | None:
        await self._collection.update_one(
            {"_id": user_id},
            {"$set": {"is_banned": banned, "updated_at": datetime.now(timezone.utc)}},
        )
        return await self.find_by_id(user_id)
