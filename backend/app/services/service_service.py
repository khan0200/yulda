from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError
from app.repositories.service_repository import ServiceRepository
from app.schemas.service import ServicePostCreate, ServicePostUpdate
from app.services.listing_helpers import assert_can_modify, owner_summary


class ServicePostService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = ServiceRepository(db)

    async def create_post(self, owner: dict[str, Any], payload: ServicePostCreate) -> dict[str, Any]:
        doc = payload.model_dump()
        if doc.get("location"):
            doc["location"] = payload.location.model_dump()
        doc["owner_id"] = owner["_id"]
        doc["owner"] = owner_summary(owner)
        return await self._repo.create(doc)

    async def get_post(self, service_id: str) -> dict[str, Any]:
        post = await self._repo.find_by_id(service_id)
        if not post:
            raise NotFoundError("Service post not found")
        return post

    async def list_posts(
        self,
        category: str | None,
        city: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list(category=category, city=city, page=page, page_size=page_size)

    async def update_post(self, service_id: str, user: dict[str, Any], payload: ServicePostUpdate) -> dict[str, Any]:
        post = await self.get_post(service_id)
        assert_can_modify(post, user)
        updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
        updated = await self._repo.update(post["_id"], updates)
        assert updated is not None
        return updated

    async def delete_post(self, service_id: str, user: dict[str, Any]) -> None:
        post = await self.get_post(service_id)
        assert_can_modify(post, user)
        await self._repo.delete(post["_id"])
