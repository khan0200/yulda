import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def _create_marketplace_listing(client, token) -> str:
    response = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "ELECTRONICS",
            "title": "Laptop",
            "description": "desc",
            "price": 500000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(token),
    )
    return response.json()["data"]["id"]


async def _create_community_post(client, token) -> str:
    response = await client.post(
        "/api/v1/community/posts",
        json={"category": "QUESTION", "title": "Hello", "body": "Anyone know a good dentist?"},
        headers=auth_headers(token),
    )
    return response.json()["data"]["id"]


async def test_toggle_favorite_requires_auth(client):
    token = await signup_and_login(client, "owner@example.com", "Owner")
    listing_id = await _create_marketplace_listing(client, token)

    client.cookies.clear()
    response = await client.post(f"/api/v1/favorites/MARKETPLACE/{listing_id}/toggle")
    assert response.status_code == 401


async def test_toggle_favorite_marks_and_unmarks_listing(client):
    owner_token = await signup_and_login(client, "owner2@example.com", "Owner2")
    liker_token = await signup_and_login(client, "liker@example.com", "Liker")
    listing_id = await _create_marketplace_listing(client, owner_token)

    like = await client.post(f"/api/v1/favorites/MARKETPLACE/{listing_id}/toggle", headers=auth_headers(liker_token))
    assert like.status_code == 200
    body = like.json()["data"]
    assert body["is_favorited"] is True
    assert body["like_count"] == 1

    get_listing = await client.get(f"/api/v1/marketplace/listings/{listing_id}")
    assert get_listing.json()["data"]["like_count"] == 1

    unlike = await client.post(f"/api/v1/favorites/MARKETPLACE/{listing_id}/toggle", headers=auth_headers(liker_token))
    assert unlike.status_code == 200
    body = unlike.json()["data"]
    assert body["is_favorited"] is False
    assert body["like_count"] == 0


async def test_toggle_favorite_on_community_post(client):
    owner_token = await signup_and_login(client, "owner3@example.com", "Owner3")
    liker_token = await signup_and_login(client, "liker2@example.com", "Liker2")
    post_id = await _create_community_post(client, owner_token)

    like = await client.post(f"/api/v1/favorites/COMMUNITY/{post_id}/toggle", headers=auth_headers(liker_token))
    assert like.status_code == 200
    assert like.json()["data"]["like_count"] == 1

    get_post = await client.get(f"/api/v1/community/posts/{post_id}")
    assert get_post.json()["data"]["like_count"] == 1


async def test_toggle_favorite_rejects_missing_target(client):
    token = await signup_and_login(client, "ghost@example.com", "Ghost")
    response = await client.post(
        "/api/v1/favorites/MARKETPLACE/000000000000000000000000/toggle", headers=auth_headers(token)
    )
    assert response.status_code == 404


async def test_list_my_favorites_returns_toggled_ids(client):
    owner_token = await signup_and_login(client, "owner4@example.com", "Owner4")
    liker_token = await signup_and_login(client, "liker3@example.com", "Liker3")
    listing_id = await _create_marketplace_listing(client, owner_token)

    empty = await client.get("/api/v1/favorites/MARKETPLACE/mine", headers=auth_headers(liker_token))
    assert empty.json()["data"] == []

    await client.post(f"/api/v1/favorites/MARKETPLACE/{listing_id}/toggle", headers=auth_headers(liker_token))

    mine = await client.get("/api/v1/favorites/MARKETPLACE/mine", headers=auth_headers(liker_token))
    assert mine.json()["data"] == [listing_id]
