import logging

import httpx

from app.core.config import settings
from app.core.exceptions import ValidationError

logger = logging.getLogger("yulda.turnstile")

VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


async def verify_turnstile_token(token: str, remote_ip: str | None = None) -> None:
    """Raises ValidationError if the token is missing/invalid. No-op when disabled."""
    if not settings.TURNSTILE_ENABLED:
        return

    if not token:
        raise ValidationError("Bot verification is required")

    payload = {"secret": settings.TURNSTILE_SECRET_KEY, "response": token}
    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(VERIFY_URL, data=payload)
            result = response.json()
    except httpx.HTTPError:
        logger.exception("Turnstile verification request failed")
        raise ValidationError("Could not verify bot check. Please try again.")

    if not result.get("success"):
        logger.warning("Turnstile verification failed: %s", result.get("error-codes"))
        raise ValidationError("Bot verification failed. Please try again.")
