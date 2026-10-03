from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError
from app.repositories.auto_repository import AutoRepository
from app.schemas.auto import AutoListingCreate, AutoListingUpdate
from app.services.listing_helpers import assert_can_modify, owner_summary


class AutoService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = AutoRepository(db)

    async def create_listing(self, owner: dict[str, Any], payload: AutoListingCreate) -> dict[str, Any]:
        doc = payload.model_dump()
        if doc.get("location"):
            doc["location"] = payload.location.model_dump()
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
        listing_type: str | None,
        make: str | None,
        fuel_type: str | None,
        transmission: str | None,
        city: str | None,
        min_year: int | None,
        max_year: int | None,
        min_price: int | None,
        max_price: int | None,
        min_mileage: int | None,
        max_mileage: int | None,
        body_type: str | None,
        color: str | None,
        accident_history: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list(
            listing_type=listing_type,
            make=make,
            fuel_type=fuel_type,
            transmission=transmission,
            city=city,
            min_year=min_year,
            max_year=max_year,
            min_price=min_price,
            max_price=max_price,
            min_mileage=min_mileage,
            max_mileage=max_mileage,
            body_type=body_type,
            color=color,
            accident_history=accident_history,
            page=page,
            page_size=page_size,
        )

    async def update_listing(self, listing_id: str, user: dict[str, Any], payload: AutoListingUpdate) -> dict[str, Any]:
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
