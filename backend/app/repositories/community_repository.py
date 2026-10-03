from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class CommunityRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._posts = db.community_posts
        self._comments = db.community_comments

    async def create_post(self, doc: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc["created_at"] = now
        doc["updated_at"] = now
        doc["comment_count"] = 0
        doc["like_count"] = 0
        result = await self._posts.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def find_post_by_id(self, post_id: str | ObjectId) -> dict[str, Any] | None:
        if isinstance(post_id, str):
            if not ObjectId.is_valid(post_id):
                return None
            post_id = ObjectId(post_id)
        return await self._posts.find_one({"_id": post_id})

    async def list_posts(
        self,
        category: str | None = None,
        city: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        query: dict[str, Any] = {}
        if category:
            query["category"] = category
        if city:
            query["city"] = city

        total = await self._posts.count_documents(query)
        cursor = (
            self._posts.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items, total

    async def update_post(self, post_id: ObjectId, updates: dict[str, Any]) -> dict[str, Any] | None:
        updates["updated_at"] = datetime.now(timezone.utc)
        await self._posts.update_one({"_id": post_id}, {"$set": updates})
        return await self.find_post_by_id(post_id)

    async def delete_post(self, post_id: ObjectId) -> None:
        await self._posts.delete_one({"_id": post_id})
        await self._comments.delete_many({"post_id": post_id})

    async def create_comment(self, doc: dict[str, Any]) -> dict[str, Any]:
        doc["created_at"] = datetime.now(timezone.utc)
        result = await self._comments.insert_one(doc)
        doc["_id"] = result.inserted_id
        await self._posts.update_one({"_id": doc["post_id"]}, {"$inc": {"comment_count": 1}})
        return doc

    async def list_comments(self, post_id: ObjectId, page: int = 1, page_size: int = 50) -> tuple[list[dict[str, Any]], int]:
        query = {"post_id": post_id}
        total = await self._comments.count_documents(query)
        cursor = (
            self._comments.find(query)
            .sort("created_at", 1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items, total
