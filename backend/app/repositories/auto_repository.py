from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class AutoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.auto_listings

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
        listing_type: str | None = None,
        make: str | None = None,
        fuel_type: str | None = None,
        transmission: str | None = None,
        city: str | None = None,
        min_year: int | None = None,
        max_year: int | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        status: str | None = "ACTIVE",
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        query: dict[str, Any] = {}
        if listing_type:
            query["listing_type"] = listing_type
        if make:
            query["make"] = make
        if fuel_type:
            query["fuel_type"] = fuel_type
        if transmission:
            query["transmission"] = transmission
        if city:
            query["city"] = city
        if status:
            query["status"] = status
        if min_year is not None or max_year is not None:
            year_filter: dict[str, Any] = {}
            if min_year is not None:
                year_filter["$gte"] = min_year
            if max_year is not None:
                year_filter["$lte"] = max_year
            query["year"] = year_filter
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

    async def update(self, listing_id: ObjectId, updates: dict[str, Any]) -> dict[str, Any] | None:
        updates["updated_at"] = datetime.now(timezone.utc)
        await self._collection.update_one({"_id": listing_id}, {"$set": updates})
        return await self.find_by_id(listing_id)

    async def delete(self, listing_id: ObjectId) -> None:
        await self._collection.delete_one({"_id": listing_id})
