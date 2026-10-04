from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class JobRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.job_posts

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc["created_at"] = now
        doc["updated_at"] = now
        doc.setdefault("status", "ACTIVE")
        doc["like_count"] = 0
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def find_by_id(self, job_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(job_id, str):
            if not ObjectId.is_valid(job_id):
                return None
            job_id = ObjectId(job_id)
        return await self._collection.find_one({"_id": job_id})

    async def list(
        self,
        post_type: str | None = None,
        category: str | None = None,
        employment_type: str | None = None,
        city: str | None = None,
        requires_korean: bool | None = None,
        visa_sponsorship: bool | None = None,
        status: str | None = "ACTIVE",
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        query: dict[str, Any] = {}
        if post_type:
            query["post_type"] = post_type
        if category:
            query["category"] = category
        if employment_type:
            query["employment_type"] = employment_type
        if city:
            query["city"] = city
        if requires_korean is not None:
            query["requires_korean"] = requires_korean
        if visa_sponsorship is not None:
            query["visa_sponsorship"] = visa_sponsorship
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

    async def list_by_owner(
        self, owner_id: ObjectId, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        query = {"owner_id": owner_id}
        total = await self._collection.count_documents(query)
        cursor = (
            self._collection.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items, total

    async def update(self, job_id: ObjectId, updates: dict[str, Any]) -> dict[str, Any] | None:
        updates["updated_at"] = datetime.now(timezone.utc)
        await self._collection.update_one({"_id": job_id}, {"$set": updates})
        return await self.find_by_id(job_id)

    async def delete(self, job_id: ObjectId) -> None:
        await self._collection.delete_one({"_id": job_id})
