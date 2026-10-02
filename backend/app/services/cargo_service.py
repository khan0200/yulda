from datetime import datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.cargo_repository import CargoRepository
from app.schemas.cargo import CargoPostCreate, CargoPostUpdate
from app.services.listing_helpers import assert_can_modify, owner_summary


class CargoService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = CargoRepository(db)

    async def create_post(self, owner: dict[str, Any], payload: CargoPostCreate) -> dict[str, Any]:
        doc = payload.model_dump()
        doc["owner_id"] = owner["_id"]
        doc["owner"] = owner_summary(owner)
        return await self._repo.create(doc)

    async def get_post(self, post_id: str) -> dict[str, Any]:
        post = await self._repo.find_by_id(post_id)
        if not post:
            raise NotFoundError("Post not found")
        return post

    async def search(
        self,
        post_type: str | None,
        from_city: str | None,
        to_city: str | None,
        date: datetime | None,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.search(post_type, from_city, to_city, date, page, page_size)

    async def search_nearby_dates(
        self,
        post_type: str | None,
        from_city: str,
        to_city: str,
        center_date: datetime,
        window_days: int = 5,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        return await self._repo.search_nearby_dates(post_type, from_city, to_city, center_date, window_days, limit)

    async def update_post(self, post_id: str, user: dict[str, Any], payload: CargoPostUpdate) -> dict[str, Any]:
        post = await self.get_post(post_id)
        assert_can_modify(post, user)
        updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
        updated = await self._repo.update(post["_id"], updates)
        assert updated is not None
        return updated

    async def deactivate_post(self, post_id: str, user: dict[str, Any]) -> dict[str, Any]:
        post = await self.get_post(post_id)
        assert_can_modify(post, user)
        updated = await self._repo.update(post["_id"], {"status": "EXPIRED"})
        assert updated is not None
        return updated

    async def repost(self, post_id: str, user: dict[str, Any], new_departure_at: datetime) -> dict[str, Any]:
        post = await self.get_post(post_id)
        assert_can_modify(post, user)
        if new_departure_at <= datetime.now(timezone.utc):
            raise ValidationError("New departure time must be in the future")
        updated = await self._repo.update(post["_id"], {"status": "ACTIVE", "departure_at": new_departure_at})
        assert updated is not None
        return updated

    async def delete_post(self, post_id: str, user: dict[str, Any]) -> None:
        post = await self.get_post(post_id)
        assert_can_modify(post, user)
        await self._repo.delete(post["_id"])
