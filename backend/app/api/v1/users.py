from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis

from app.api.deps import get_current_user, get_db, get_redis_client
from app.core.exceptions import ValidationError
from app.core.responses import ApiResponse
from app.core.security import hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import ChangePasswordRequest, DeleteAccountRequest, UserPublic, UserUpdate
from app.services.auth_service import REFRESH_TOKEN_PREFIX

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


@router.post("/me/change-password", response_model=ApiResponse[None])
async def change_my_password(
    payload: ChangePasswordRequest,
    user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    if not verify_password(payload.current_password, user["password_hash"]):
        raise ValidationError("Current password is incorrect")
    repo = UserRepository(db)
    await repo.set_password_hash(user["_id"], hash_password(payload.new_password))
    return ApiResponse(data=None, message="Password changed successfully")


@router.delete("/me", response_model=ApiResponse[None])
async def delete_my_account(
    payload: DeleteAccountRequest,
    user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
    redis: Redis = Depends(get_redis_client),
):
    if not verify_password(payload.password, user["password_hash"]):
        raise ValidationError("Password is incorrect")
    await UserRepository(db).delete(user["_id"])
    await redis.delete(f"{REFRESH_TOKEN_PREFIX}{user['_id']}")
    return ApiResponse(data=None, message="Account deleted")
