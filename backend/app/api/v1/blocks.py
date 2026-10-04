from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse
from app.schemas.block import BlockCreate, BlockPublic
from app.services.block_service import BlockService

router = APIRouter(prefix="/blocks", tags=["blocks"])


def get_block_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> BlockService:
    return BlockService(db)


@router.get("", response_model=ApiResponse[list[BlockPublic]])
async def list_my_blocks(
    user: dict = Depends(get_current_user),
    service: BlockService = Depends(get_block_service),
):
    blocks = await service.list_my_blocks(user)
    return ApiResponse(data=[BlockPublic.model_validate(block) for block in blocks])


@router.post("", response_model=ApiResponse[BlockPublic], status_code=201)
async def block_user(
    payload: BlockCreate,
    user: dict = Depends(get_current_user),
    service: BlockService = Depends(get_block_service),
):
    block = await service.block_user(user, payload.blocked_user_id)
    return ApiResponse(data=BlockPublic.model_validate(block), message="User blocked")


@router.delete("/{user_id}", response_model=ApiResponse[None])
async def unblock_user(
    user_id: str,
    user: dict = Depends(get_current_user),
    service: BlockService = Depends(get_block_service),
):
    await service.unblock_user(user, user_id)
    return ApiResponse(data=None, message="User unblocked")
