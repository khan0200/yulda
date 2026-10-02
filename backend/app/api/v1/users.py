from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserPublic, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=ApiResponse[UserPublic])
async def get_my_profile(user: dict = Depends(get_current_user)):
    return ApiResponse(data=UserPublic.model_validate(user))


@router.patch("/me", response_model=ApiResponse[UserPublic])
async def update_my_profile(
    payload: UserUpdate,
    user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
    if payload.location is not None:
        updates["location"] = payload.location.model_dump()
    updated = await UserRepository(db).update(user["_id"], updates)
    return ApiResponse(data=UserPublic.model_validate(updated), message="Profile updated")
