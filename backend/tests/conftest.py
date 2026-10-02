import os

os.environ["ENV"] = "test"

import pytest
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.api import deps
from app.core.fake_redis import FakeRedis
from app.main import app


@pytest.fixture(autouse=True)
def _patch_infra():
    mock_client = AsyncMongoMockClient()
    mock_db = mock_client["yulda_test"]
    fake_redis = FakeRedis()

    app.dependency_overrides[deps.get_db] = lambda: mock_db
    app.dependency_overrides[deps.get_redis_client] = lambda: fake_redis
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
