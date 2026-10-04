from __future__ import annotations

from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.block_repository import BlockRepository
from app.repositories.user_repository import UserRepository


class BlockService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._repo = BlockRepository(db)
        self._users = UserRepository(db)

    async def block_user(self, user: dict[str, Any], blocked_user_id: str) -> dict[str, Any]:
        if not ObjectId.is_valid(blocked_user_id):
            raise NotFoundError("User not found")
        blocked_object_id = ObjectId(blocked_user_id)
        if blocked_object_id == user["_id"]:
            raise ValidationError("You cannot block yourself")

        target = await self._users.find_by_id(blocked_object_id)
        if not target:
            raise NotFoundError("User not found")

        existing = await self._repo.find(user["_id"], blocked_object_id)
        block = existing or await self._repo.create(user["_id"], blocked_object_id)
        block["blocked_user"] = target
        return block

    async def unblock_user(self, user: dict[str, Any], blocked_user_id: str) -> None:
        if not ObjectId.is_valid(blocked_user_id):
            raise NotFoundError("User not found")
        await self._repo.delete(user["_id"], ObjectId(blocked_user_id))

    async def list_my_blocks(self, user: dict[str, Any]) -> list[dict[str, Any]]:
        blocks = await self._repo.list_by_blocker(user["_id"])
        result = []
        for block in blocks:
            blocked_user = await self._users.find_by_id(block["blocked_id"])
            if not blocked_user:
                continue
            block["blocked_user"] = blocked_user
            result.append(block)
        return result

    async def is_blocked_either_direction(self, user_a: ObjectId, user_b: ObjectId) -> bool:
        return await self._repo.exists_either_direction(user_a, user_b)
