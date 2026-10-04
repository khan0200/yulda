from datetime import datetime, time, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError
from app.repositories.housing_repository import HousingRepository
from app.schemas.housing import HousingCreate, HousingUpdate
from app.services.listing_helpers import assert_can_modify, owner_summary


class HousingService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = HousingRepository(db)

    async def create_listing(self, owner: dict[str, Any], payload: HousingCreate) -> dict[str, Any]:
        doc = payload.model_dump()
        if doc.get("location"):
            doc["location"] = payload.location.model_dump()
        if doc.get("move_in_date"):
            doc["move_in_date"] = datetime.combine(payload.move_in_date, time.min)
        doc["amenities"] = [a.value for a in payload.amenities]
        if payload.direction is not None:
            doc["direction"] = payload.direction.value
        doc["owner_id"] = owner["_id"]
        doc["owner"] = owner_summary(owner)
        return await self._repo.create(doc)

    async def get_listing(self, listing_id: str) -> dict[str, Any]:
        listing = await self._repo.find_by_id(listing_id)
        if not listing:
            raise NotFoundError("Listing not found")
        return listing

    async def list_listings(
        self,
        housing_type: str | None,
        city: str | None,
        min_deposit: int | None,
        max_deposit: int | None,
        min_rent: int | None,
        max_rent: int | None,
        amenities: list[str] | None,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list(
            housing_type=housing_type,
            city=city,
            min_deposit=min_deposit,
            max_deposit=max_deposit,
            min_rent=min_rent,
            max_rent=max_rent,
            amenities=amenities,
            page=page,
            page_size=page_size,
        )

    async def update_listing(self, listing_id: str, user: dict[str, Any], payload: HousingUpdate) -> dict[str, Any]:
        listing = await self.get_listing(listing_id)
        assert_can_modify(listing, user)
        updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
        if "amenities" in updates:
            updates["amenities"] = [a.value if hasattr(a, "value") else a for a in updates["amenities"]]
        if "direction" in updates and hasattr(updates["direction"], "value"):
            updates["direction"] = updates["direction"].value
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
