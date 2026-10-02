from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.user import UserRole
from app.repositories.community_repository import CommunityRepository
from app.schemas.community import CommentCreate, PostCreate, PostUpdate


def _author_summary(user: dict[str, Any]) -> dict[str, Any]:
    return {"_id": user["_id"], "name": user["name"], "avatar": user.get("avatar")}


class CommunityService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = CommunityRepository(db)

    async def create_post(self, author: dict[str, Any], payload: PostCreate) -> dict[str, Any]:
        doc = payload.model_dump()
        if doc.get("location"):
            doc["location"] = payload.location.model_dump()
        doc["author_id"] = author["_id"]
        doc["author"] = _author_summary(author)
        return await self._repo.create_post(doc)

    async def get_post(self, post_id: str) -> dict[str, Any]:
        post = await self._repo.find_post_by_id(post_id)
        if not post:
            raise NotFoundError("Post not found")
        return post

    async def list_posts(
        self, category: str | None, city: str | None, page: int, page_size: int
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list_posts(category=category, city=city, page=page, page_size=page_size)

    async def update_post(self, post_id: str, user: dict[str, Any], payload: PostUpdate) -> dict[str, Any]:
        post = await self.get_post(post_id)
        self._assert_can_modify(post, user)
        updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
        updated = await self._repo.update_post(post["_id"], updates)
        assert updated is not None
        return updated

    async def delete_post(self, post_id: str, user: dict[str, Any]) -> None:
        post = await self.get_post(post_id)
        self._assert_can_modify(post, user)
        await self._repo.delete_post(post["_id"])

    async def add_comment(self, post_id: str, author: dict[str, Any], payload: CommentCreate) -> dict[str, Any]:
        post = await self.get_post(post_id)
        doc = {
            "post_id": post["_id"],
            "body": payload.body,
            "author_id": author["_id"],
            "author": _author_summary(author),
        }
        return await self._repo.create_comment(doc)

    async def list_comments(self, post_id: str, page: int, page_size: int) -> tuple[list[dict[str, Any]], int]:
        post = await self.get_post(post_id)
        return await self._repo.list_comments(post["_id"], page=page, page_size=page_size)

    @staticmethod
    def _assert_can_modify(post: dict[str, Any], user: dict[str, Any]) -> None:
        is_author = post["author_id"] == user["_id"]
        is_admin = UserRole.ADMIN.value in user.get("roles", [])
        if not (is_author or is_admin):
            raise ForbiddenError("You can only modify your own posts")
