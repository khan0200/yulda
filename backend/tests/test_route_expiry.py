from datetime import datetime, timedelta, timezone

import pytest

from app.repositories.route_repository import RouteRepository

pytestmark = pytest.mark.asyncio


async def test_deactivate_expired_only_affects_posts_past_grace_period(db):
    repo = RouteRepository(db)
    now = datetime.now(timezone.utc)

    recently_departed = await repo.create(
        {
            "post_type": "OFFER",
            "stops": [{"name": "Busan", "country": "KR"}, {"name": "Seoul", "country": "KR"}],
            "departure_at": now - timedelta(minutes=30),
            "contact_phone": "010-1111-1111",
            "owner_id": "u1",
            "owner": {"_id": "u1", "name": "A", "avatar": None},
        }
    )
    long_departed = await repo.create(
        {
            "post_type": "OFFER",
            "stops": [{"name": "Busan", "country": "KR"}, {"name": "Seoul", "country": "KR"}],
            "departure_at": now - timedelta(hours=2),
            "contact_phone": "010-2222-2222",
            "owner_id": "u2",
            "owner": {"_id": "u2", "name": "B", "avatar": None},
        }
    )
    future = await repo.create(
        {
            "post_type": "OFFER",
            "stops": [{"name": "Busan", "country": "KR"}, {"name": "Seoul", "country": "KR"}],
            "departure_at": now + timedelta(hours=5),
            "contact_phone": "010-3333-3333",
            "owner_id": "u3",
            "owner": {"_id": "u3", "name": "C", "avatar": None},
        }
    )

    expired_count = await repo.deactivate_expired(now)
    assert expired_count == 1

    assert (await repo.find_by_id(recently_departed["_id"]))["status"] == "ACTIVE"
    assert (await repo.find_by_id(long_departed["_id"]))["status"] == "EXPIRED"
    assert (await repo.find_by_id(future["_id"]))["status"] == "ACTIVE"
