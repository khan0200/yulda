from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse, PaginatedData
from app.schemas.conversation import ConversationCreate, ConversationPublic, MessageCreate, MessagePublic
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


def get_conversation_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> ConversationService:
    return ConversationService(db)


@router.get("", response_model=ApiResponse[PaginatedData[ConversationPublic]])
async def list_my_conversations(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    user: dict = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    items, total = await service.list_my_conversations(user, page=page, page_size=page_size)
    return ApiResponse(
        data=PaginatedData(
            items=[ConversationPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("", response_model=ApiResponse[ConversationPublic], status_code=201)
async def start_conversation(
    payload: ConversationCreate,
    user: dict = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    convo = await service.get_or_create(user, payload)
    convo.setdefault("unread_count", 0)
    return ApiResponse(data=ConversationPublic.model_validate(convo), message="Conversation ready")


@router.get("/{conversation_id}/messages", response_model=ApiResponse[PaginatedData[MessagePublic]])
async def list_messages(
    conversation_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    user: dict = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    items, total = await service.list_messages(conversation_id, user, page=page, page_size=page_size)
    return ApiResponse(
        data=PaginatedData(
            items=[MessagePublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/{conversation_id}/messages", response_model=ApiResponse[MessagePublic], status_code=201)
async def send_message(
    conversation_id: str,
    payload: MessageCreate,
    user: dict = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    message = await service.send_message(conversation_id, user, payload)
    return ApiResponse(data=MessagePublic.model_validate(message), message="Message sent")


@router.post("/{conversation_id}/read", response_model=ApiResponse[None])
async def mark_conversation_read(
    conversation_id: str,
    user: dict = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    await service.mark_read(conversation_id, user)
    return ApiResponse(data=None, message="Conversation marked as read")
