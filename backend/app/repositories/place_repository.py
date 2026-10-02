import re
from datetime import datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase


class PlaceRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.places

    async def search(self, query: str, country: str | None, limit: int = 10) -> list[dict[str, Any]]:
        pattern = re.compile("^" + re.escape(query.strip()), re.IGNORECASE)
        mongo_query: dict[str, Any] = {
            "$or": [
                {"name": pattern},
                {"ascii_name": pattern},
                {"alt_names": pattern},
            ]
        }
        if country:
            mongo_query["country"] = country

        cursor = (
            self._collection.find(mongo_query)
            .sort([("usage_count", -1), ("population", -1)])
            .limit(limit)
        )
        return await cursor.to_list(length=limit)

    async def find_exact(self, name: str, country: str) -> dict[str, Any] | None:
        return await self._collection.find_one(
            {"name": {"$regex": f"^{re.escape(name.strip())}$", "$options": "i"}, "country": country}
        )

    async def add_or_increment(self, name: str, country: str) -> dict[str, Any]:
        existing = await self.find_exact(name, country)
        if existing:
            await self._collection.update_one({"_id": existing["_id"]}, {"$inc": {"usage_count": 1}})
            existing["usage_count"] = existing.get("usage_count", 0) + 1
            return existing

        doc = {
            "name": name.strip(),
            "ascii_name": name.strip(),
            "alt_names": [],
            "country": country,
            "admin1": None,
            "population": 0,
            "lat": None,
            "lon": None,
            "source": "USER",
            "usage_count": 1,
            "created_at": datetime.now(timezone.utc),
        }
        result = await self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def count(self) -> int:
        return await self._collection.count_documents({})

    async def bulk_insert_seed(self, docs: list[dict[str, Any]]) -> None:
        if not docs:
            return
        await self._collection.insert_many(docs, ordered=False)
