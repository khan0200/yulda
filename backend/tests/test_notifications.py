import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def _trigger_like_notification(client, owner_token, liker_token) -> None:
    listing = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "ELECTRONICS",
            "title": "Notify Test Item",
            "description": "desc",
            "price": 10000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(owner_token),
    )
    listing_id = listing.json()["data"]["id"]
    await client.post(f"/api/v1/favorites/MARKETPLACE/{listing_id}/toggle", headers=auth_headers(liker_token))


async def test_liking_a_listing_notifies_the_owner(client):
    owner_token = await signup_and_login(client, "notifyowner@example.com", "NotifyOwner")
    liker_token = await signup_and_login(client, "notifyliker@example.com", "NotifyLiker")

    await _trigger_like_notification(client, owner_token, liker_token)

    notifications = await client.get("/api/v1/notifications", headers=auth_headers(owner_token))
    items = notifications.json()["data"]["items"]
    assert any(n["type"] == "LISTING_LIKED" and n["title"] == "NotifyLiker" for n in items)


async def test_liking_own_listing_does_not_notify(client):
    owner_token = await signup_and_login(client, "selfliker@example.com", "SelfLiker")
    listing = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "OTHER",
            "title": "Self Like Item",
            "description": "desc",
            "price": 5000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(owner_token),
    )
    listing_id = listing.json()["data"]["id"]
    await client.post(f"/api/v1/favorites/MARKETPLACE/{listing_id}/toggle", headers=auth_headers(owner_token))

    notifications = await client.get("/api/v1/notifications", headers=auth_headers(owner_token))
    assert notifications.json()["data"]["total"] == 0


async def test_mark_notification_read(client):
    owner_token = await signup_and_login(client, "readowner@example.com", "ReadOwner")
    liker_token = await signup_and_login(client, "readliker@example.com", "ReadLiker")
    await _trigger_like_notification(client, owner_token, liker_token)

    notifications = await client.get("/api/v1/notifications", headers=auth_headers(owner_token))
    notification_id = notifications.json()["data"]["items"][0]["id"]

    mark = await client.post(f"/api/v1/notifications/{notification_id}/read", headers=auth_headers(owner_token))
    assert mark.status_code == 200
    assert mark.json()["data"]["is_read"] is True

    unread = await client.get("/api/v1/notifications/unread-count", headers=auth_headers(owner_token))
    assert unread.json()["data"]["unread_count"] == 0


async def test_mark_all_notifications_read(client):
    owner_token = await signup_and_login(client, "allreadowner@example.com", "AllReadOwner")
    liker1_token = await signup_and_login(client, "allreadliker1@example.com", "AllReadLiker1")
    liker2_token = await signup_and_login(client, "allreadliker2@example.com", "AllReadLiker2")
    await _trigger_like_notification(client, owner_token, liker1_token)
    await _trigger_like_notification(client, owner_token, liker2_token)

    before = await client.get("/api/v1/notifications/unread-count", headers=auth_headers(owner_token))
    assert before.json()["data"]["unread_count"] == 2

    mark_all = await client.post("/api/v1/notifications/read-all", headers=auth_headers(owner_token))
    assert mark_all.status_code == 200

    after = await client.get("/api/v1/notifications/unread-count", headers=auth_headers(owner_token))
    assert after.json()["data"]["unread_count"] == 0


async def test_notifications_require_auth(client):
    response = await client.get("/api/v1/notifications")
    assert response.status_code == 401
