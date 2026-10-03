from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class ServiceRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.service_posts

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc["created_at"] = now
        doc["updated_at"] = now
        doc.setdefault("status", "ACTIVE")
        doc["like_count"] = 0
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def find_by_id(self, service_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(service_id, str):
            if not ObjectId.is_valid(service_id):
                return None
            service_id = ObjectId(service_id)
        return await self._collection.find_one({"_id": service_id})

    async def list(
        self,
        category: str | None = None,
        city: str | None = None,
        status: str | None = "ACTIVE",
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        query: dict[str, Any] = {}
        if category:
            query["category"] = category
        if city:
            query["city"] = city
        if status:
            query["status"] = status

        total = await self._collection.count_documents(query)
        cursor = (
            self._collection.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items, total

    async def update(self, service_id: ObjectId, updates: dict[str, Any]) -> dict[str, Any] | None:
        updates["updated_at"] = datetime.now(timezone.utc)
        await self._collection.update_one({"_id": service_id}, {"$set": updates})
        return await self.find_by_id(service_id)

    async def delete(self, service_id: ObjectId) -> None:
        await self._collection.delete_one({"_id": service_id})
