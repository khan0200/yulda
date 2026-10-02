import asyncio
import logging
from datetime import datetime, timezone

from app.core.database import get_database
from app.repositories.cargo_repository import CargoRepository
from app.repositories.route_repository import RouteRepository

logger = logging.getLogger("yulda.route_expiry")

CHECK_INTERVAL_SECONDS = 300


async def _run_once() -> None:
    db = get_database()
    now = datetime.now(timezone.utc)

    route_count = await RouteRepository(db).deactivate_expired(now)
    cargo_count = await CargoRepository(db).deactivate_expired(now)

    if route_count or cargo_count:
        logger.info("Auto-expired %d route posts and %d cargo posts", route_count, cargo_count)


async def run_expiry_loop() -> None:
    while True:
        try:
            await _run_once()
        except Exception:
            logger.exception("Error while auto-expiring route/cargo posts")
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)
