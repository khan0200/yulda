from datetime import datetime, timedelta, timezone

import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


def _future_iso(hours: int = 48) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


async def test_create_international_cargo_offer(client):
    token = await signup_and_login(client, "courier1@example.com", "Courier1")
    payload = {
        "post_type": "OFFER",
        "stops": [
            {"name": "Incheon", "country": "KR"},
            {"name": "Seoul", "country": "KR"},
            {"name": "Tashkent", "country": "UZ"},
            {"name": "Andijon", "country": "UZ"},
            {"name": "Asaka", "country": "UZ"},
        ],
        "departure_at": _future_iso(),
        "accepted_categories": ["DOCUMENTS", "MEDICINE", "PERSONAL_ITEMS"],
        "rejected_categories": ["PHONE", "PERFUME"],
        "max_weight_kg": 38,
        "notes": "Dorixonadan ham olib beramiz",
        "contact_phone": "010-9804-1247",
    }
    response = await client.post("/api/v1/cargo", json=payload, headers=auth_headers(token))
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["max_weight_kg"] == 38
    assert "DOCUMENTS" in body["accepted_categories"]
    assert "PHONE" in body["rejected_categories"]
    assert body["owner"]["name"] == "Courier1"


async def test_create_cargo_requires_auth(client):
    response = await client.post(
        "/api/v1/cargo",
        json={
            "post_type": "OFFER",
            "stops": [{"name": "Incheon", "country": "KR"}, {"name": "Tashkent", "country": "UZ"}],
            "departure_at": _future_iso(),
            "contact_phone": "010-0000-0000",
        },
    )
    assert response.status_code == 401


async def test_search_finds_mid_route_international_subsequence(client):
    """Mirrors the real-world example: a courier flies Kyongsang -> Degu ->
    Incheon -> Toshkent -> Andijon -> Asaka. A sender searching Incheon -> Andijon
    should find this post even though their leg is only part of the full route."""
    token = await signup_and_login(client, "courier2@example.com", "Courier2")
    await client.post(
        "/api/v1/cargo",
        json={
            "post_type": "OFFER",
            "stops": [
                {"name": "Kyongsang", "country": "KR"},
                {"name": "Degu", "country": "KR"},
                {"name": "Incheon", "country": "KR"},
                {"name": "Toshkent", "country": "UZ"},
                {"name": "Andijon", "country": "UZ"},
                {"name": "Asaka", "country": "UZ"},
            ],
            "departure_at": _future_iso(),
            "accepted_categories": ["DOCUMENTS"],
            "contact_phone": "010-1111-2222",
        },
        headers=auth_headers(token),
    )

    response = await client.get(
        "/api/v1/cargo/search", params={"from_city": "Incheon", "to_city": "Andijon"}
    )
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["stops"][0]["name"] == "Kyongsang"


async def test_search_filters_by_rejected_category_is_informational_only(client):
    """The platform doesn't auto-filter by category server-side search params
    beyond city/date/type — category matching is visual (shown on the card),
    consistent with the 'just connect them, let humans decide' model."""
    token = await signup_and_login(client, "courier3@example.com", "Courier3")
    await client.post(
        "/api/v1/cargo",
        json={
            "post_type": "OFFER",
            "stops": [{"name": "Seoul", "country": "KR"}, {"name": "Samarkand", "country": "UZ"}],
            "departure_at": _future_iso(),
            "rejected_categories": ["PERFUME"],
            "contact_phone": "010-3333-4444",
        },
        headers=auth_headers(token),
    )

    response = await client.get(
        "/api/v1/cargo/search", params={"from_city": "Seoul", "to_city": "Samarkand"}
    )
    data = response.json()["data"]
    assert data["total"] == 1
    assert "PERFUME" in data["items"][0]["rejected_categories"]


async def test_search_with_no_exact_date_match_suggests_nearby(client):
    token = await signup_and_login(client, "courier4@example.com", "Courier4")
    departure = datetime.now(timezone.utc) + timedelta(days=4)
    await client.post(
        "/api/v1/cargo",
        json={
            "post_type": "OFFER",
            "stops": [{"name": "Busan", "country": "KR"}, {"name": "Dushanbe", "country": "TJ"}],
            "departure_at": departure.isoformat(),
            "contact_phone": "010-5555-6666",
        },
        headers=auth_headers(token),
    )

    wrong_date = (departure + timedelta(days=1)).isoformat()
    response = await client.get(
        "/api/v1/cargo/search",
        params={"from_city": "Busan", "to_city": "Dushanbe", "date": wrong_date},
    )
    data = response.json()["data"]
    assert data["total"] == 0
    assert len(data["suggested_other_dates"]) == 1


async def test_only_owner_can_deactivate_and_delete(client):
    owner_token = await signup_and_login(client, "cargoowner@example.com", "CargoOwner")
    other_token = await signup_and_login(client, "cargostranger@example.com", "CargoStranger")

    create = await client.post(
        "/api/v1/cargo",
        json={
            "post_type": "REQUEST",
            "stops": [{"name": "Seoul", "country": "KR"}, {"name": "Bishkek", "country": "KG"}],
            "departure_at": _future_iso(),
            "contact_phone": "010-7777-8888",
        },
        headers=auth_headers(owner_token),
    )
    post_id = create.json()["data"]["id"]

    forbidden = await client.delete(f"/api/v1/cargo/{post_id}", headers=auth_headers(other_token))
    assert forbidden.status_code == 403

    allowed = await client.delete(f"/api/v1/cargo/{post_id}", headers=auth_headers(owner_token))
    assert allowed.status_code == 200


async def test_browsing_cargo_does_not_require_auth(client):
    response = await client.get("/api/v1/cargo/search")
    assert response.status_code == 200
