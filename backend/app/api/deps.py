from typing import Any

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis

from app.core.database import get_database
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.redis import get_redis
from app.core.security import decode_access_token
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> AsyncIOMotorDatabase:
    return get_database()


def get_redis_client() -> Redis:
    return get_redis()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    access_token_cookie: str | None = Cookie(default=None, alias="access_token"),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict[str, Any]:
    token = credentials.credentials if credentials else access_token_cookie
    if token is None:
        raise UnauthorizedError("Missing authentication credentials")
    try:
        payload = decode_access_token(token)
    except JWTError as exc:
        raise UnauthorizedError("Invalid or expired access token") from exc

    user = await UserRepository(db).find_by_id(payload["sub"])
    if not user:
        raise UnauthorizedError("User no longer exists")
    if user.get("is_banned"):
        raise ForbiddenError("Your account has been suspended")
    return user


def require_roles(*roles: UserRole):
    async def _check(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        user_roles = set(user.get("roles", []))
        allowed = {r.value for r in roles}
        if not user_roles & allowed:
            raise ForbiddenError("You do not have permission to perform this action")
        return user

    return _check
