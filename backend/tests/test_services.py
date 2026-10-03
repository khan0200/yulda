import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def test_create_and_get_service_post(client):
    token = await signup_and_login(client, "provider@example.com", "Provider")
    response = await client.post(
        "/api/v1/services/posts",
        json={
            "category": "BEAUTY",
            "title": "Haircut at home",
            "description": "I come to your place with full equipment",
            "price_note": "20000 won",
            "city": "Ansan",
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["title"] == "Haircut at home"
    assert body["status"] == "ACTIVE"
    assert body["owner"]["name"] == "Provider"
    assert body["like_count"] == 0

    service_id = body["id"]
    get_response = await client.get(f"/api/v1/services/posts/{service_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["price_note"] == "20000 won"


async def test_create_service_post_requires_auth(client):
    response = await client.post(
        "/api/v1/services/posts",
        json={
            "category": "REPAIR",
            "title": "Phone screen repair",
            "description": "Same-day repair",
            "contact_value": "010-0000-0000",
        },
    )
    assert response.status_code == 401


async def test_list_services_filters_by_category_and_city(client):
    token = await signup_and_login(client, "servicer@example.com", "Servicer")
    await client.post(
        "/api/v1/services/posts",
        json={
            "category": "TUTORING",
            "title": "Korean tutoring",
            "description": "desc",
            "city": "Seoul",
            "contact_value": "010-1234-5678",
        },
        headers=auth_headers(token),
    )
    await client.post(
        "/api/v1/services/posts",
        json={
            "category": "TUTORING",
            "title": "Math tutoring",
            "description": "desc",
            "city": "Busan",
            "contact_value": "010-1234-5678",
        },
        headers=auth_headers(token),
    )

    response = await client.get("/api/v1/services/posts", params={"category": "TUTORING", "city": "Seoul"})
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Korean tutoring"


async def test_only_owner_can_delete_service_post(client):
    owner_token = await signup_and_login(client, "serviceowner@example.com", "ServiceOwner")
    other_token = await signup_and_login(client, "servicestranger@example.com", "ServiceStranger")

    create = await client.post(
        "/api/v1/services/posts",
        json={
            "category": "CLEANING",
            "title": "House cleaning",
            "description": "desc",
            "contact_value": "010-9999-0000",
        },
        headers=auth_headers(owner_token),
    )
    service_id = create.json()["data"]["id"]

    forbidden = await client.delete(f"/api/v1/services/posts/{service_id}", headers=auth_headers(other_token))
    assert forbidden.status_code == 403

    allowed = await client.delete(f"/api/v1/services/posts/{service_id}", headers=auth_headers(owner_token))
    assert allowed.status_code == 200

    gone = await client.get(f"/api/v1/services/posts/{service_id}")
    assert gone.status_code == 404


async def test_toggle_favorite_on_service_post(client):
    owner_token = await signup_and_login(client, "serviceowner2@example.com", "ServiceOwner2")
    liker_token = await signup_and_login(client, "serviceliker@example.com", "ServiceLiker")

    create = await client.post(
        "/api/v1/services/posts",
        json={
            "category": "PHOTOGRAPHY",
            "title": "Portrait photography",
            "description": "desc",
            "contact_value": "010-5555-5555",
        },
        headers=auth_headers(owner_token),
    )
    service_id = create.json()["data"]["id"]

    like = await client.post(f"/api/v1/favorites/SERVICES/{service_id}/toggle", headers=auth_headers(liker_token))
    assert like.status_code == 200
    assert like.json()["data"]["like_count"] == 1

    get_post = await client.get(f"/api/v1/services/posts/{service_id}")
    assert get_post.json()["data"]["like_count"] == 1
