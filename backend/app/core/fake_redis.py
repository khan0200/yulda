import asyncio
import time
from datetime import timedelta


class FakeRedis:
    """Minimal in-process stand-in for the subset of Redis used by the app.

    Only for local development when no real Redis is reachable. Data is
    lost on restart and never shared across processes.
    """

    def __init__(self) -> None:
        self._store: dict[str, tuple[str, float | None]] = {}
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: str, ex: int | float | timedelta | None = None) -> None:
        expires_at: float | None = None
        if ex is not None:
            seconds = ex.total_seconds() if hasattr(ex, "total_seconds") else float(ex)
            expires_at = time.monotonic() + seconds
        async with self._lock:
            self._store[key] = (value, expires_at)

    async def get(self, key: str) -> str | None:
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expires_at = entry
            if expires_at is not None and time.monotonic() > expires_at:
                del self._store[key]
                return None
            return value

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)

    async def ping(self) -> bool:
        return True

    async def aclose(self) -> None:
        self._store.clear()
