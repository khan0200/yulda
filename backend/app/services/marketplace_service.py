from datetime import datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError
from app.repositories.marketplace_repository import MarketplaceRepository
from app.schemas.marketplace import ListingCreate, ListingUpdate
from app.services.listing_helpers import assert_can_modify, owner_summary


class MarketplaceService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = MarketplaceRepository(db)

    async def create_listing(self, seller: dict[str, Any], payload: ListingCreate) -> dict[str, Any]:
        doc = payload.model_dump()
        if doc.get("location"):
            doc["location"] = payload.location.model_dump()
        doc["owner_id"] = seller["_id"]
        doc["seller"] = owner_summary(seller)
        return await self._repo.create(doc)

    async def get_listing(self, listing_id: str) -> dict[str, Any]:
        listing = await self._repo.find_by_id(listing_id)
        if not listing:
            raise NotFoundError("Listing not found")
        return listing

    async def list_listings(
        self,
        category: str | None,
        city: str | None,
        condition: str | None,
        min_price: int | None,
        max_price: int | None,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list(
            category=category,
            city=city,
            condition=condition,
            min_price=min_price,
            max_price=max_price,
            page=page,
            page_size=page_size,
        )

    async def update_listing(self, listing_id: str, user: dict[str, Any], payload: ListingUpdate) -> dict[str, Any]:
        listing = await self.get_listing(listing_id)
        assert_can_modify(listing, user)
        updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
        updated = await self._repo.update(listing["_id"], updates)
        assert updated is not None
        return updated

    async def delete_listing(self, listing_id: str, user: dict[str, Any]) -> None:
        listing = await self.get_listing(listing_id)
        assert_can_modify(listing, user)
        await self._repo.delete(listing["_id"])

    async def list_my_listings(self, user: dict[str, Any], page: int, page_size: int) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list_by_owner(user["_id"], page=page, page_size=page_size)

    async def repost_listing(self, listing_id: str, user: dict[str, Any]) -> dict[str, Any]:
        listing = await self.get_listing(listing_id)
        assert_can_modify(listing, user)
        now = datetime.now(timezone.utc)
        updated = await self._repo.update(listing["_id"], {"created_at": now, "status": "ACTIVE"})
        assert updated is not None
        return updated
