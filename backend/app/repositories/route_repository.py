from datetime import datetime, timedelta, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.route_matching import normalize_stop_name, search_nearby_dates, search_routes


class RouteRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.route_posts

    async def create(self, doc: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc["created_at"] = now
        doc["updated_at"] = now
        doc["status"] = "ACTIVE"
        doc["stop_names_lower"] = [normalize_stop_name(s["name"]) for s in doc["stops"]]
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def find_by_id(self, post_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(post_id, str):
            if not ObjectId.is_valid(post_id):
                return None
            post_id = ObjectId(post_id)
        return await self._collection.find_one({"_id": post_id})

    async def search(
        self,
        post_type: str | None,
        from_city: str | None,
        to_city: str | None,
        date: datetime | None,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        return await search_routes(self._collection, post_type, from_city, to_city, date, page, page_size)

    async def search_nearby_dates(
        self,
        post_type: str | None,
        from_city: str,
        to_city: str,
        center_date: datetime,
        window_days: int,
        limit: int,
    ) -> list[dict[str, Any]]:
        return await search_nearby_dates(
            self._collection, post_type, from_city, to_city, center_date, window_days, limit
        )

    async def update(self, post_id: ObjectId, updates: dict[str, Any]) -> dict[str, Any] | None:
        updates["updated_at"] = datetime.now(timezone.utc)
        if "stops" in updates:
            updates["stop_names_lower"] = [normalize_stop_name(s["name"]) for s in updates["stops"]]
        await self._collection.update_one({"_id": post_id}, {"$set": updates})
        return await self.find_by_id(post_id)

    async def delete(self, post_id: ObjectId) -> None:
        await self._collection.delete_one({"_id": post_id})

    async def deactivate_expired(self, as_of: datetime) -> int:
        cutoff = as_of - timedelta(hours=1)
        result = await self._collection.update_many(
            {"status": "ACTIVE", "departure_at": {"$lt": cutoff}},
            {"$set": {"status": "EXPIRED", "updated_at": as_of}},
        )
        return result.modified_count
