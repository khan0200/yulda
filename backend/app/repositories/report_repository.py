from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class ReportRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.reports

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        doc["created_at"] = datetime.now(timezone.utc)
        doc.setdefault("status", "PENDING")
        doc.setdefault("resolved_at", None)
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def find_by_id(self, report_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(report_id, str):
            if not ObjectId.is_valid(report_id):
                return None
            report_id = ObjectId(report_id)
        return await self._collection.find_one({"_id": report_id})

    async def list(
        self, status: str | None, page: int = 1, page_size: int = 20
    ) -> tuple[list[dict[str, Any]], int]:
        query: dict[str, Any] = {"status": status} if status else {}
        total = await self._collection.count_documents(query)
        cursor = (
            self._collection.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items, total

    async def update_status(self, report_id: ObjectId, status: str) -> dict[str, Any] | None:
        await self._collection.update_one(
            {"_id": report_id},
            {"$set": {"status": status, "resolved_at": datetime.now(timezone.utc)}},
        )
        return await self.find_by_id(report_id)
