from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class MarketplaceRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.marketplace_listings

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc["created_at"] = now
        doc["updated_at"] = now
        doc.setdefault("status", "ACTIVE")
        doc["like_count"] = 0
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def find_by_id(self, listing_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(listing_id, str):
            if not ObjectId.is_valid(listing_id):
                return None
            listing_id = ObjectId(listing_id)
        return await self._collection.find_one({"_id": listing_id})

    async def list(
        self,
        category: str | None = None,
        city: str | None = None,
        condition: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        status: str | None = "ACTIVE",
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        query: dict[str, Any] = {}
        if category:
            query["category"] = category
        if city:
            query["city"] = city
        if condition:
            query["condition"] = condition
        if status:
            query["status"] = status
        if min_price is not None or max_price is not None:
            price_filter: dict[str, Any] = {}
            if min_price is not None:
                price_filter["$gte"] = min_price
            if max_price is not None:
                price_filter["$lte"] = max_price
            query["price"] = price_filter

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

    async def update(self, listing_id: ObjectId, updates: dict[str, Any]) -> dict[str, Any] | None:
        updates["updated_at"] = datetime.now(timezone.utc)
        await self._collection.update_one({"_id": listing_id}, {"$set": updates})
        return await self.find_by_id(listing_id)

    async def delete(self, listing_id: ObjectId) -> None:
        await self._collection.delete_one({"_id": listing_id})
