from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError, ValidationError
from app.models.favorite import FavoriteTargetType
from app.repositories.favorite_repository import FavoriteRepository

_TARGET_COLLECTIONS = {
    FavoriteTargetType.MARKETPLACE.value: "marketplace_listings",
    FavoriteTargetType.COMMUNITY.value: "community_posts",
    FavoriteTargetType.JOBS.value: "job_posts",
    FavoriteTargetType.SERVICES.value: "service_posts",
}


class FavoriteService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db
        self._repo = FavoriteRepository(db)

    async def toggle(self, user_id: ObjectId, target_type: str, target_id: str) -> dict[str, Any]:
        if target_type not in _TARGET_COLLECTIONS:
            raise ValidationError("Invalid favorite target type")
        if not ObjectId.is_valid(target_id):
            raise NotFoundError("Target not found")
        target_object_id = ObjectId(target_id)

        collection = self._db[_TARGET_COLLECTIONS[target_type]]
        target = await collection.find_one({"_id": target_object_id})
        if not target:
            raise NotFoundError("Target not found")

        existing = await self._repo.find(user_id, target_type, target_object_id)
        if existing:
            await self._repo.remove(user_id, target_type, target_object_id)
            await collection.update_one(
                {"_id": target_object_id, "like_count": {"$gt": 0}},
                {"$inc": {"like_count": -1}},
            )
            is_favorited = False
        else:
            await self._repo.add(user_id, target_type, target_object_id)
            await collection.update_one(
                {"_id": target_object_id},
                {"$inc": {"like_count": 1}},
            )
            is_favorited = True

        result = await collection.find_one({"_id": target_object_id})
        return {
            "is_favorited": is_favorited,
            "like_count": result.get("like_count", 0) if result else 0,
        }

    async def list_favorited_ids(self, user_id: ObjectId, target_type: str) -> set[str]:
        return await self._repo.list_target_ids_for_user(user_id, target_type)
