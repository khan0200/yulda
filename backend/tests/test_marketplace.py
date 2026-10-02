import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def test_create_and_get_listing(client):
    token = await signup_and_login(client, "seller@example.com", "Seller")
    response = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "ELECTRONICS",
            "title": "iPhone 17 Air White 256GB",
            "description": "Battery 91%, like new",
            "price": 920000,
            "condition": "USED",
            "contact_method": "KAKAOTALK",
            "contact_value": "kakao_id_123",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["title"] == "iPhone 17 Air White 256GB"
    assert body["price"] == 920000
    assert body["status"] == "ACTIVE"
    assert body["seller"]["name"] == "Seller"

    listing_id = body["id"]
    get_response = await client.get(f"/api/v1/marketplace/listings/{listing_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["condition"] == "USED"


async def test_create_listing_requires_auth(client):
    response = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "FREE",
            "title": "Free sofa",
            "description": "Pickup only",
            "price": 0,
            "condition": "USED",
            "contact_method": "PHONE",
            "contact_value": "010-1234-5678",
        },
    )
    assert response.status_code == 401


async def test_list_listings_filters_by_category_and_price(client):
    token = await signup_and_login(client, "filterer@example.com", "Filterer")
    for category, price in [("ELECTRONICS", 500000), ("FURNITURE", 50000), ("ELECTRONICS", 2000000)]:
        await client.post(
            "/api/v1/marketplace/listings",
            json={
                "category": category,
                "title": f"Item {price}",
                "description": "desc",
                "price": price,
                "condition": "NEW",
                "contact_method": "CHAT",
                "contact_value": "chat-handle",
            },
            headers=auth_headers(token),
        )

    response = await client.get(
        "/api/v1/marketplace/listings",
        params={"category": "ELECTRONICS", "max_price": 1000000},
    )
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["price"] == 500000


async def test_only_owner_can_delete_listing(client):
    owner_token = await signup_and_login(client, "owner@example.com", "Owner")
    other_token = await signup_and_login(client, "stranger@example.com", "Stranger")

    create = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "BIKES",
            "title": "Road bike",
            "description": "desc",
            "price": 300000,
            "condition": "USED",
            "contact_method": "PHONE",
            "contact_value": "010-0000-0000",
        },
        headers=auth_headers(owner_token),
    )
    listing_id = create.json()["data"]["id"]

    forbidden = await client.delete(f"/api/v1/marketplace/listings/{listing_id}", headers=auth_headers(other_token))
    assert forbidden.status_code == 403

    allowed = await client.delete(f"/api/v1/marketplace/listings/{listing_id}", headers=auth_headers(owner_token))
    assert allowed.status_code == 200

    gone = await client.get(f"/api/v1/marketplace/listings/{listing_id}")
    assert gone.status_code == 404


async def test_update_listing_status_to_sold(client):
    token = await signup_and_login(client, "marker@example.com", "Marker")
    create = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "CLOTHING",
            "title": "Jacket",
            "description": "desc",
            "price": 40000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(token),
    )
    listing_id = create.json()["data"]["id"]

    update = await client.patch(
        f"/api/v1/marketplace/listings/{listing_id}",
        json={"status": "SOLD"},
        headers=auth_headers(token),
    )
    assert update.status_code == 200
    assert update.json()["data"]["status"] == "SOLD"

    active_listings = await client.get("/api/v1/marketplace/listings")
    ids = [item["id"] for item in active_listings.json()["data"]["items"]]
    assert listing_id not in ids
