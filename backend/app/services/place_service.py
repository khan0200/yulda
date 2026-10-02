from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.place_repository import PlaceRepository
from app.schemas.place import PlaceCreate


class PlaceService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = PlaceRepository(db)

    async def search(self, query: str, country: str | None, limit: int = 10) -> list[dict[str, Any]]:
        query = query.strip()
        if not query:
            return []
        return await self._repo.search(query, country, limit)

    async def learn(self, payload: PlaceCreate) -> dict[str, Any]:
        return await self._repo.add_or_increment(payload.name, payload.country.value)
