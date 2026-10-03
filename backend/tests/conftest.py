import os

os.environ["ENV"] = "test"

import pytest
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.api import deps
from app.core.config import settings
from app.core.fake_redis import FakeRedis
from app.main import app

settings.TURNSTILE_ENABLED = False


@pytest.fixture(autouse=True)
def _patch_infra():
    mock_client = AsyncMongoMockClient()
    mock_db = mock_client["yulda_test"]
    fake_redis = FakeRedis()

    app.dependency_overrides[deps.get_db] = lambda: mock_db
    app.dependency_overrides[deps.get_redis_client] = lambda: fake_redis
    yield mock_db
    app.dependency_overrides.clear()


@pytest.fixture
def db(_patch_infra):
    return _patch_infra


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def signup_and_login(client, email: str, name: str) -> str:
    await client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": "StrongPass123", "name": name},
    )
    login = await client.post("/api/v1/auth/login", json={"email": email, "password": "StrongPass123"})
    return login.json()["data"]["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
