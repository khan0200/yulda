from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class HousingRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.housing_listings

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc["created_at"] = now
        doc["updated_at"] = now
        doc.setdefault("status", "ACTIVE")
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
        housing_type: str | None = None,
        city: str | None = None,
        min_deposit: int | None = None,
        max_deposit: int | None = None,
        min_rent: int | None = None,
        max_rent: int | None = None,
        amenities: list[str] | None = None,
        status: str | None = "ACTIVE",
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        query: dict[str, Any] = {}
        if housing_type:
            query["housing_type"] = housing_type
        if city:
            query["city"] = city
        if status:
            query["status"] = status
        if amenities:
            query["amenities"] = {"$all": amenities}
        if min_deposit is not None or max_deposit is not None:
            deposit_filter: dict[str, Any] = {}
            if min_deposit is not None:
                deposit_filter["$gte"] = min_deposit
            if max_deposit is not None:
                deposit_filter["$lte"] = max_deposit
            query["deposit"] = deposit_filter
        if min_rent is not None or max_rent is not None:
            rent_filter: dict[str, Any] = {}
            if min_rent is not None:
                rent_filter["$gte"] = min_rent
            if max_rent is not None:
                rent_filter["$lte"] = max_rent
            query["monthly_rent"] = rent_filter

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
