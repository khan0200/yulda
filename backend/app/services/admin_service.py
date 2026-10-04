from __future__ import annotations

from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.user_repository import UserRepository

_CONTENT_COLLECTIONS = {
    "MARKETPLACE": "marketplace_listings",
    "HOUSING": "housing_listings",
    "AUTO": "auto_listings",
    "JOBS": "job_posts",
    "SERVICES": "service_posts",
    "COMMUNITY": "community_posts",
}


class AdminService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db
        self._users = UserRepository(db)

    async def list_users(
        self, search: str | None, page: int, page_size: int
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._users.list(page=page, page_size=page_size, search=search)

    async def set_user_banned(self, admin: dict[str, Any], user_id: str, banned: bool) -> dict[str, Any]:
        if not ObjectId.is_valid(user_id):
            raise NotFoundError("User not found")
        target_object_id = ObjectId(user_id)
        if target_object_id == admin["_id"]:
            raise ValidationError("You cannot ban your own account")

        target = await self._users.find_by_id(target_object_id)
        if not target:
            raise NotFoundError("User not found")

        return await self._users.set_banned(target_object_id, banned)

    async def remove_content(self, target_type: str, content_id: str) -> None:
        if target_type not in _CONTENT_COLLECTIONS:
            raise ValidationError("Invalid content type")
        if not ObjectId.is_valid(content_id):
            raise NotFoundError("Content not found")

        collection = self._db[_CONTENT_COLLECTIONS[target_type]]
        result = await collection.delete_one({"_id": ObjectId(content_id)})
        if result.deleted_count == 0:
            raise NotFoundError("Content not found")
