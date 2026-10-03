import httpx
import pytest

from app.core.config import settings
from app.services.turnstile_service import verify_turnstile_token

pytestmark = pytest.mark.asyncio


async def test_disabled_turnstile_skips_verification_entirely(monkeypatch):
    monkeypatch.setattr(settings, "TURNSTILE_ENABLED", False)
    # No token at all, and no network mocking — if this didn't short-circuit,
    # it would raise (missing token) or try a real network call and fail.
    await verify_turnstile_token("")


async def test_enabled_turnstile_rejects_empty_token(monkeypatch):
    monkeypatch.setattr(settings, "TURNSTILE_ENABLED", True)
    monkeypatch.setattr(settings, "TURNSTILE_SECRET_KEY", "fake-secret")

    from app.core.exceptions import ValidationError

    with pytest.raises(ValidationError):
        await verify_turnstile_token("")


async def test_enabled_turnstile_accepts_valid_token(monkeypatch):
    monkeypatch.setattr(settings, "TURNSTILE_ENABLED", True)
    monkeypatch.setattr(settings, "TURNSTILE_SECRET_KEY", "fake-secret")

    async def fake_post(self, url, data=None, **kwargs):
        return httpx.Response(200, json={"success": True}, request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    await verify_turnstile_token("valid-token-from-widget")


async def test_enabled_turnstile_rejects_failed_verification(monkeypatch):
    monkeypatch.setattr(settings, "TURNSTILE_ENABLED", True)
    monkeypatch.setattr(settings, "TURNSTILE_SECRET_KEY", "fake-secret")

    async def fake_post(self, url, data=None, **kwargs):
        return httpx.Response(
            200, json={"success": False, "error-codes": ["invalid-input-response"]}, request=httpx.Request("POST", url)
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    from app.core.exceptions import ValidationError

    with pytest.raises(ValidationError):
        await verify_turnstile_token("tampered-or-expired-token")


async def test_signup_succeeds_without_token_when_turnstile_disabled(client):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "no-turnstile@example.com", "password": "StrongPass123", "name": "No Turnstile"},
    )
    assert response.status_code == 201
