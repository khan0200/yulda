import logging
import secrets
import uuid
from datetime import timedelta
from typing import Any

from jose import JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis

from app.core.config import settings
from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import UserRole, VerificationStatus
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenPair, UserCreate

logger = logging.getLogger("yulda.auth")

REFRESH_TOKEN_PREFIX = "refresh_token:"
PASSWORD_RESET_PREFIX = "password_reset:"


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase, redis: Redis):
        self._users = UserRepository(db)
        self._redis = redis

    async def signup(self, payload: UserCreate) -> tuple[dict[str, Any], TokenPair]:
        existing = await self._users.find_by_email(payload.email)
        if existing:
            raise ConflictError("An account with this email already exists")

        user_doc = {
            "email": payload.email,
            "phone": payload.phone,
            "password_hash": hash_password(payload.password),
            "name": payload.name,
            "avatar": None,
            "roles": [r.value for r in payload.roles],
            "verification_status": VerificationStatus.UNVERIFIED.value,
            "location": None,
        }
        user = await self._users.create(user_doc)
        tokens = await self._issue_tokens(str(user["_id"]), user["roles"])
        return user, tokens

    async def login(self, email: str, password: str) -> tuple[dict[str, Any], TokenPair]:
        user = await self._users.find_by_email(email)
        if not user or not verify_password(password, user["password_hash"]):
            raise UnauthorizedError("Invalid email or password")
        tokens = await self._issue_tokens(str(user["_id"]), user["roles"])
        return user, tokens

    async def refresh(self, refresh_token: str) -> TokenPair:
        try:
            payload = decode_refresh_token(refresh_token)
        except JWTError as exc:
            raise UnauthorizedError("Invalid or expired refresh token") from exc

        user_id = payload["sub"]
        jti = payload["jti"]
        stored_jti = await self._redis.get(f"{REFRESH_TOKEN_PREFIX}{user_id}")
        if stored_jti != jti:
            raise UnauthorizedError("Refresh token has been revoked")

        user = await self._users.find_by_id(user_id)
        if not user:
            raise UnauthorizedError("User no longer exists")

        return await self._issue_tokens(user_id, user["roles"])

    async def logout(self, user_id: str) -> None:
        await self._redis.delete(f"{REFRESH_TOKEN_PREFIX}{user_id}")

    async def _issue_tokens(self, user_id: str, roles: list[str]) -> TokenPair:
        access = create_access_token(user_id, roles)
        jti = uuid.uuid4().hex
        refresh = create_refresh_token(user_id, jti)
        await self._redis.set(
            f"{REFRESH_TOKEN_PREFIX}{user_id}",
            jti,
            ex=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return TokenPair(access_token=access, refresh_token=refresh)

    async def request_password_reset(self, email: str) -> str | None:
        user = await self._users.find_by_email(email)
        if not user:
            # Do not reveal whether the email exists.
            return None
        token = secrets.token_urlsafe(32)
        await self._redis.set(f"{PASSWORD_RESET_PREFIX}{token}", str(user["_id"]), ex=timedelta(hours=1))
        logger.info("Password reset token generated for user %s (dev-mode: email delivery not configured)", user["_id"])
        return token

    async def reset_password(self, token: str, new_password: str) -> None:
        key = f"{PASSWORD_RESET_PREFIX}{token}"
        user_id = await self._redis.get(key)
        if not user_id:
            raise UnauthorizedError("Invalid or expired reset token")
        from bson import ObjectId

        await self._users.set_password_hash(ObjectId(user_id), hash_password(new_password))
        await self._redis.delete(key)
        await self._redis.delete(f"{REFRESH_TOKEN_PREFIX}{user_id}")
