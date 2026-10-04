from __future__ import annotations

from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.repositories.block_repository import BlockRepository
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.schemas.conversation import ConversationCreate, MessageCreate
from app.schemas.conversation import MessagePublic
from app.services.notification_service import NotificationService
from app.websocket.manager import manager


def _participant_summary(user: dict[str, Any]) -> dict[str, Any]:
    return {"_id": user["_id"], "name": user["name"], "avatar": user.get("avatar")}


class ConversationService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._conversations = ConversationRepository(db)
        self._messages = MessageRepository(db)
        self._users = UserRepository(db)
        self._blocks = BlockRepository(db)
        self._notifications = NotificationService(db)

    async def get_or_create(self, current_user: dict[str, Any], payload: ConversationCreate) -> dict[str, Any]:
        if payload.target_user_id == str(current_user["_id"]):
            raise ValidationError("Cannot start a conversation with yourself")
        target = await self._users.find_by_id(payload.target_user_id)
        if not target:
            raise NotFoundError("User not found")

        if await self._blocks.exists_either_direction(current_user["_id"], target["_id"]):
            raise ForbiddenError("You cannot message this user")

        existing = await self._conversations.find_between(current_user["_id"], target["_id"], payload.listing_id)
        if existing:
            return existing

        doc = {
            "participant_ids": [current_user["_id"], target["_id"]],
            "participants": [_participant_summary(current_user), _participant_summary(target)],
            "listing_type": payload.listing_type.value if payload.listing_type else None,
            "listing_id": payload.listing_id,
            "listing_title": payload.listing_title,
            "last_message_preview": None,
            "last_message_at": None,
        }
        return await self._conversations.create(doc)

    async def get_conversation(self, conversation_id: str, user: dict[str, Any]) -> dict[str, Any]:
        convo = await self._conversations.find_by_id(conversation_id)
        if not convo:
            raise NotFoundError("Conversation not found")
        if user["_id"] not in convo["participant_ids"]:
            raise ForbiddenError("You are not a participant of this conversation")
        return convo

    async def list_my_conversations(
        self, user: dict[str, Any], page: int, page_size: int
    ) -> tuple[list[dict[str, Any]], int]:
        items, total = await self._conversations.list_for_user(user["_id"], page=page, page_size=page_size)
        for item in items:
            item["unread_count"] = await self._messages.count_unread(item["_id"], user["_id"])
        return items, total

    async def list_messages(
        self, conversation_id: str, user: dict[str, Any], page: int, page_size: int
    ) -> tuple[list[dict[str, Any]], int]:
        convo = await self.get_conversation(conversation_id, user)
        return await self._messages.list_for_conversation(convo["_id"], page=page, page_size=page_size)

    async def send_message(
        self, conversation_id: str, user: dict[str, Any], payload: MessageCreate
    ) -> dict[str, Any]:
        convo = await self.get_conversation(conversation_id, user)
        recipient_id = next(pid for pid in convo["participant_ids"] if pid != user["_id"])
        if await self._blocks.exists_either_direction(user["_id"], recipient_id):
            raise ForbiddenError("You cannot message this user")
        doc = {"conversation_id": convo["_id"], "sender_id": user["_id"], "body": payload.body}
        message = await self._messages.create(doc)

        preview = payload.body if len(payload.body) <= 140 else payload.body[:137] + "..."
        await self._conversations.touch_last_message(convo["_id"], preview, message["created_at"])

        message_public = MessagePublic.model_validate(message).model_dump(mode="json")
        await manager.send_to_user(
            str(recipient_id),
            {"event": "message", "conversation_id": str(convo["_id"]), "message": message_public},
        )

        await self._notifications.create_and_push(
            recipient_id,
            "NEW_MESSAGE",
            title=user["name"],
            body=preview,
            link=f"/messages/{convo['_id']}",
        )

        return message

    async def mark_read(self, conversation_id: str, user: dict[str, Any]) -> None:
        convo = await self.get_conversation(conversation_id, user)
        await self._messages.mark_read(convo["_id"], user["_id"])
