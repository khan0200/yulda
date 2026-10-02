import logging
from typing import Union

import redis.asyncio as redis
from redis.exceptions import RedisError

from app.core.config import settings
from app.core.fake_redis import FakeRedis

logger = logging.getLogger("yulda.redis")

_redis: Union[redis.Redis, FakeRedis, None] = None


def get_redis() -> Union[redis.Redis, FakeRedis]:
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def connect_to_redis() -> None:
    global _redis

    client = redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    try:
        await client.ping()
        _redis = client
        logger.info("Connected to Redis at %s", settings.REDIS_URL)
    except RedisError:
        await client.aclose()
        if settings.ENV != "development":
            logger.exception("Failed to connect to Redis")
            raise
        logger.warning(
            "No Redis reachable at %s — falling back to an in-memory mock for local "
            "development. State will NOT persist across restarts or be shared between "
            "processes. Install/run real Redis (or docker compose up) for production-like behavior.",
            settings.REDIS_URL,
        )
        _redis = FakeRedis()


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
