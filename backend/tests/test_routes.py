from datetime import datetime, timedelta, timezone

import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


def _future_iso(hours: int = 48) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


def _stops(*names: str) -> list[dict]:
    return [{"name": name, "country": "KR"} for name in names]


async def _create_route_post(client, token: str, **overrides) -> dict:
    payload = {
        "post_type": "OFFER",
        "stops": _stops("Busan", "Daegu", "Cheongju", "Icheon", "Baran", "Incheon", "Seoul"),
        "departure_at": _future_iso(),
        "vehicle_info": "KIA K5",
        "seats": 4,
        "contact_phone": "010-1111-2222",
        **overrides,
    }
    response = await client.post("/api/v1/routes", json=payload, headers=auth_headers(token))
    return response


async def test_create_route_post_with_multi_stop_route(client):
    token = await signup_and_login(client, "driver1@example.com", "Driver1")
    response = await _create_route_post(client, token)
    assert response.status_code == 201
    body = response.json()["data"]
    assert len(body["stops"]) == 7
    assert body["stops"][0]["name"] == "Busan"
    assert body["status"] == "ACTIVE"
    assert body["owner"]["name"] == "Driver1"


async def test_create_route_post_requires_auth(client):
    response = await client.post(
        "/api/v1/routes",
        json={
            "post_type": "OFFER",
            "stops": _stops("Busan", "Seoul"),
            "departure_at": _future_iso(),
            "contact_phone": "010-0000-0000",
        },
    )
    assert response.status_code == 401


async def test_create_route_rejects_consecutive_duplicate_stops(client):
    token = await signup_and_login(client, "dupdriver@example.com", "DupDriver")
    response = await _create_route_post(client, token, stops=_stops("Busan", "Busan", "Seoul"))
    assert response.status_code == 422


async def test_create_route_rejects_fewer_than_two_stops(client):
    token = await signup_and_login(client, "onestop@example.com", "OneStop")
    response = await _create_route_post(client, token, stops=_stops("Busan"))
    assert response.status_code == 422


async def test_search_finds_mid_route_subsequence(client):
    """A passenger searching Cheongju -> Baran should find a driver whose
    full route is Busan -> Daegu -> Cheongju -> Icheon -> Baran -> Incheon -> Seoul,
    even though neither endpoint matches the passenger's search exactly."""
    token = await signup_and_login(client, "driver2@example.com", "Driver2")
    await _create_route_post(client, token)

    response = await client.get(
        "/api/v1/routes/search", params={"from_city": "Cheongju", "to_city": "Baran"}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["stops"][0]["name"] == "Busan"


async def test_search_rejects_reversed_direction(client):
    """Searching Baran -> Cheongju (reverse order) should NOT match a route
    that goes Cheongju -> Baran, since direction matters for a real trip."""
    token = await signup_and_login(client, "driver3@example.com", "Driver3")
    await _create_route_post(client, token)

    response = await client.get(
        "/api/v1/routes/search", params={"from_city": "Baran", "to_city": "Cheongju"}
    )
    data = response.json()["data"]
    assert data["total"] == 0


async def test_search_filters_by_post_type(client):
    token = await signup_and_login(client, "driver4@example.com", "Driver4")
    await _create_route_post(client, token, post_type="OFFER")
    await _create_route_post(client, token, post_type="REQUEST", seats=None)

    response = await client.get("/api/v1/routes/search", params={"post_type": "REQUEST"})
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["post_type"] == "REQUEST"


async def test_search_exact_date_with_no_match_suggests_nearby_dates(client):
    token = await signup_and_login(client, "driver5@example.com", "Driver5")
    departure = datetime.now(timezone.utc) + timedelta(days=3)
    await _create_route_post(client, token, departure_at=departure.isoformat())

    wrong_date = (departure + timedelta(days=2)).isoformat()
    response = await client.get(
        "/api/v1/routes/search",
        params={"from_city": "Busan", "to_city": "Seoul", "date": wrong_date},
    )
    data = response.json()["data"]
    assert data["total"] == 0
    assert len(data["suggested_other_dates"]) == 1
    assert data["suggested_other_dates"][0]["stops"][0]["name"] == "Busan"


async def test_search_exact_date_match_does_not_need_suggestions(client):
    token = await signup_and_login(client, "driver6@example.com", "Driver6")
    departure = datetime.now(timezone.utc) + timedelta(days=3)
    await _create_route_post(client, token, departure_at=departure.isoformat())

    response = await client.get(
        "/api/v1/routes/search",
        params={"from_city": "Busan", "to_city": "Seoul", "date": departure.isoformat()},
    )
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["suggested_other_dates"] == []


async def test_only_owner_can_deactivate_post(client):
    owner_token = await signup_and_login(client, "routeowner@example.com", "RouteOwner")
    other_token = await signup_and_login(client, "routestranger@example.com", "RouteStranger")

    create = await _create_route_post(client, owner_token)
    post_id = create.json()["data"]["id"]

    forbidden = await client.post(f"/api/v1/routes/{post_id}/deactivate", headers=auth_headers(other_token))
    assert forbidden.status_code == 403

    allowed = await client.post(f"/api/v1/routes/{post_id}/deactivate", headers=auth_headers(owner_token))
    assert allowed.status_code == 200
    assert allowed.json()["data"]["status"] == "EXPIRED"


async def test_deactivated_post_does_not_appear_in_search(client):
    token = await signup_and_login(client, "driver7@example.com", "Driver7")
    create = await _create_route_post(client, token)
    post_id = create.json()["data"]["id"]

    await client.post(f"/api/v1/routes/{post_id}/deactivate", headers=auth_headers(token))

    response = await client.get("/api/v1/routes/search", params={"from_city": "Busan", "to_city": "Seoul"})
    assert response.json()["data"]["total"] == 0


async def test_repost_reactivates_with_new_departure_time(client):
    token = await signup_and_login(client, "driver8@example.com", "Driver8")
    create = await _create_route_post(client, token)
    post_id = create.json()["data"]["id"]

    await client.post(f"/api/v1/routes/{post_id}/deactivate", headers=auth_headers(token))

    new_time = _future_iso(hours=72)
    repost = await client.post(
        f"/api/v1/routes/{post_id}/repost",
        json={"departure_at": new_time},
        headers=auth_headers(token),
    )
    assert repost.status_code == 200
    assert repost.json()["data"]["status"] == "ACTIVE"

    response = await client.get("/api/v1/routes/search", params={"from_city": "Busan", "to_city": "Seoul"})
    assert response.json()["data"]["total"] == 1


async def test_repost_rejects_past_departure_time(client):
    token = await signup_and_login(client, "driver9@example.com", "Driver9")
    create = await _create_route_post(client, token)
    post_id = create.json()["data"]["id"]

    past_time = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
    response = await client.post(
        f"/api/v1/routes/{post_id}/repost",
        json={"departure_at": past_time},
        headers=auth_headers(token),
    )
    assert response.status_code == 422
    assert response.json()["error_code"] == "VALIDATION_ERROR"


async def test_owner_can_edit_seat_count(client):
    token = await signup_and_login(client, "driver10@example.com", "Driver10")
    create = await _create_route_post(client, token, seats=4)
    post_id = create.json()["data"]["id"]

    response = await client.patch(
        f"/api/v1/routes/{post_id}", json={"seats": 2}, headers=auth_headers(token)
    )
    assert response.status_code == 200
    assert response.json()["data"]["seats"] == 2


async def test_only_owner_can_delete_post(client):
    owner_token = await signup_and_login(client, "deleter@example.com", "Deleter")
    other_token = await signup_and_login(client, "nondeleter@example.com", "NonDeleter")

    create = await _create_route_post(client, owner_token)
    post_id = create.json()["data"]["id"]

    forbidden = await client.delete(f"/api/v1/routes/{post_id}", headers=auth_headers(other_token))
    assert forbidden.status_code == 403

    allowed = await client.delete(f"/api/v1/routes/{post_id}", headers=auth_headers(owner_token))
    assert allowed.status_code == 200

    gone = await client.get(f"/api/v1/routes/{post_id}")
    assert gone.status_code == 404


async def test_browsing_routes_does_not_require_auth(client):
    response = await client.get("/api/v1/routes/search")
    assert response.status_code == 200
