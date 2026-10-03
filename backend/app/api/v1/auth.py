from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis

from app.api.deps import get_current_user, get_db, get_redis_client
from app.core.responses import ApiResponse
from app.schemas.user import (
    ForgotPasswordRequest,
    RefreshRequest,
    ResetPasswordRequest,
    TokenPair,
    UserCreate,
    UserLogin,
    UserPublic,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: AsyncIOMotorDatabase = Depends(get_db), redis: Redis = Depends(get_redis_client)) -> AuthService:
    return AuthService(db, redis)


@router.post("/signup", response_model=ApiResponse[TokenPair], status_code=201)
async def signup(payload: UserCreate, request: Request, service: AuthService = Depends(get_auth_service)):
    _, tokens = await service.signup(payload, remote_ip=request.client.host if request.client else None)
    return ApiResponse(data=tokens, message="Account created successfully")


@router.post("/login", response_model=ApiResponse[TokenPair])
async def login(payload: UserLogin, request: Request, service: AuthService = Depends(get_auth_service)):
    _, tokens = await service.login(
        payload.email,
        payload.password,
        turnstile_token=payload.turnstile_token,
        remote_ip=request.client.host if request.client else None,
    )
    return ApiResponse(data=tokens, message="Logged in successfully")


@router.post("/refresh", response_model=ApiResponse[TokenPair])
async def refresh(payload: RefreshRequest, service: AuthService = Depends(get_auth_service)):
    tokens = await service.refresh(payload.refresh_token)
    return ApiResponse(data=tokens, message="Token refreshed")


@router.post("/logout", response_model=ApiResponse[None])
async def logout(
    user: dict = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
):
    await service.logout(str(user["_id"]))
    return ApiResponse(data=None, message="Logged out successfully")


@router.post("/forgot-password", response_model=ApiResponse[None])
async def forgot_password(payload: ForgotPasswordRequest, request: Request, service: AuthService = Depends(get_auth_service)):
    await service.request_password_reset(
        payload.email,
        turnstile_token=payload.turnstile_token,
        remote_ip=request.client.host if request.client else None,
    )
    return ApiResponse(data=None, message="If that email exists, a reset link has been sent")


@router.post("/reset-password", response_model=ApiResponse[None])
async def reset_password(payload: ResetPasswordRequest, service: AuthService = Depends(get_auth_service)):
    await service.reset_password(payload.token, payload.new_password)
    return ApiResponse(data=None, message="Password reset successfully")


@router.get("/me", response_model=ApiResponse[UserPublic])
async def me(user: dict = Depends(get_current_user)):
    return ApiResponse(data=UserPublic.model_validate(user))
