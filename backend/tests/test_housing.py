import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def test_create_and_get_listing(client):
    token = await signup_and_login(client, "landlord@example.com", "Landlord")
    response = await client.post(
        "/api/v1/housing/listings",
        json={
            "housing_type": "ONE_ROOM",
            "title": "Cozy wonroom near Inha University",
            "description": "5 min walk to campus",
            "deposit": 5000000,
            "monthly_rent": 450000,
            "maintenance_fee": 50000,
            "amenities": ["FRIDGE", "WASHER", "AC"],
            "city": "Incheon",
            "metro_station": "Inha Univ.",
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["housing_type"] == "ONE_ROOM"
    assert body["deposit"] == 5000000
    assert set(body["amenities"]) == {"FRIDGE", "WASHER", "AC"}
    assert body["owner"]["name"] == "Landlord"

    listing_id = body["id"]
    get_response = await client.get(f"/api/v1/housing/listings/{listing_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["metro_station"] == "Inha Univ."


async def test_create_listing_requires_auth(client):
    response = await client.post(
        "/api/v1/housing/listings",
        json={
            "housing_type": "TWO_ROOM",
            "title": "Two room",
            "description": "desc",
            "deposit": 1000000,
            "monthly_rent": 600000,
            "contact_value": "010-0000-0000",
        },
    )
    assert response.status_code == 401


async def test_list_listings_filters_by_type_and_rent_range(client):
    token = await signup_and_login(client, "owner2@example.com", "Owner2")
    for housing_type, rent in [("ONE_ROOM", 400000), ("TWO_ROOM", 800000), ("ONE_ROOM", 900000)]:
        await client.post(
            "/api/v1/housing/listings",
            json={
                "housing_type": housing_type,
                "title": f"Listing {rent}",
                "description": "desc",
                "deposit": 1000000,
                "monthly_rent": rent,
                "contact_value": "010-1234-5678",
            },
            headers=auth_headers(token),
        )

    response = await client.get(
        "/api/v1/housing/listings",
        params={"housing_type": "ONE_ROOM", "max_rent": 500000},
    )
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["monthly_rent"] == 400000


async def test_only_owner_can_update_listing(client):
    owner_token = await signup_and_login(client, "realowner@example.com", "RealOwner")
    other_token = await signup_and_login(client, "nosyneighbor@example.com", "NosyNeighbor")

    create = await client.post(
        "/api/v1/housing/listings",
        json={
            "housing_type": "ROOMMATE",
            "title": "Roommate wanted",
            "description": "desc",
            "deposit": 2000000,
            "monthly_rent": 300000,
            "contact_value": "010-9999-8888",
        },
        headers=auth_headers(owner_token),
    )
    listing_id = create.json()["data"]["id"]

    forbidden = await client.patch(
        f"/api/v1/housing/listings/{listing_id}",
        json={"monthly_rent": 1},
        headers=auth_headers(other_token),
    )
    assert forbidden.status_code == 403

    allowed = await client.patch(
        f"/api/v1/housing/listings/{listing_id}",
        json={"status": "RENTED"},
        headers=auth_headers(owner_token),
    )
    assert allowed.status_code == 200
    assert allowed.json()["data"]["status"] == "RENTED"


async def test_move_in_date_round_trips(client):
    token = await signup_and_login(client, "dated@example.com", "Dated")
    response = await client.post(
        "/api/v1/housing/listings",
        json={
            "housing_type": "APARTMENT",
            "title": "Apartment",
            "description": "desc",
            "deposit": 10000000,
            "monthly_rent": 1200000,
            "move_in_date": "2026-11-01",
            "contact_value": "010-5555-5555",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    assert response.json()["data"]["move_in_date"] == "2026-11-01"
