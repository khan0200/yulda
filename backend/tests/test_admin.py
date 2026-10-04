import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def _make_admin(db, email: str) -> None:
    await db.users.update_one({"email": email}, {"$set": {"roles": ["ADMIN"]}})


async def _user_id(client, token) -> str:
    me = await client.get("/api/v1/users/me", headers=auth_headers(token))
    return me.json()["data"]["id"]


async def test_non_admin_cannot_list_users(client):
    token = await signup_and_login(client, "notadmin@example.com", "NotAdmin")
    response = await client.get("/api/v1/admin/users", headers=auth_headers(token))
    assert response.status_code == 403


async def test_admin_can_list_users(client, db):
    await signup_and_login(client, "listtarget@example.com", "ListTarget")
    admin_token = await signup_and_login(client, "admin2@example.com", "Admin2")
    await _make_admin(db, "admin2@example.com")

    response = await client.get("/api/v1/admin/users?search=ListTarget", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["data"]["total"] == 1


async def test_admin_can_ban_and_unban_user(client, db):
    target_token = await signup_and_login(client, "bantarget@example.com", "BanTarget")
    target_id = await _user_id(client, target_token)
    admin_token = await signup_and_login(client, "admin3@example.com", "Admin3")
    await _make_admin(db, "admin3@example.com")

    ban = await client.post(f"/api/v1/admin/users/{target_id}/ban", headers=auth_headers(admin_token))
    assert ban.status_code == 200
    assert ban.json()["data"]["is_banned"] is True

    blocked_request = await client.get("/api/v1/users/me", headers=auth_headers(target_token))
    assert blocked_request.status_code == 403

    unban = await client.post(f"/api/v1/admin/users/{target_id}/unban", headers=auth_headers(admin_token))
    assert unban.status_code == 200
    assert unban.json()["data"]["is_banned"] is False

    restored_request = await client.get("/api/v1/users/me", headers=auth_headers(target_token))
    assert restored_request.status_code == 200


async def test_admin_cannot_ban_self(client, db):
    admin_token = await signup_and_login(client, "admin4@example.com", "Admin4")
    await _make_admin(db, "admin4@example.com")
    admin_id = await _user_id(client, admin_token)

    response = await client.post(f"/api/v1/admin/users/{admin_id}/ban", headers=auth_headers(admin_token))
    assert response.status_code == 422


async def test_non_admin_cannot_ban(client):
    token1 = await signup_and_login(client, "notadmin2@example.com", "NotAdmin2")
    token2 = await signup_and_login(client, "notadmin3@example.com", "NotAdmin3")
    target_id = await _user_id(client, token2)

    response = await client.post(f"/api/v1/admin/users/{target_id}/ban", headers=auth_headers(token1))
    assert response.status_code == 403


async def test_admin_can_remove_content(client, db):
    owner_token = await signup_and_login(client, "contentowner@example.com", "ContentOwner")
    admin_token = await signup_and_login(client, "admin5@example.com", "Admin5")
    await _make_admin(db, "admin5@example.com")

    listing = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "ELECTRONICS",
            "title": "Admin Remove Target",
            "description": "desc",
            "price": 10000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(owner_token),
    )
    listing_id = listing.json()["data"]["id"]

    remove = await client.delete(
        f"/api/v1/admin/content/MARKETPLACE/{listing_id}", headers=auth_headers(admin_token)
    )
    assert remove.status_code == 200

    get_again = await client.get(f"/api/v1/marketplace/listings/{listing_id}")
    assert get_again.status_code == 404


async def test_admin_remove_content_requires_admin(client):
    owner_token = await signup_and_login(client, "contentowner2@example.com", "ContentOwner2")
    listing = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "ELECTRONICS",
            "title": "Admin Remove Target 2",
            "description": "desc",
            "price": 10000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(owner_token),
    )
    listing_id = listing.json()["data"]["id"]

    remove = await client.delete(
        f"/api/v1/admin/content/MARKETPLACE/{listing_id}", headers=auth_headers(owner_token)
    )
    assert remove.status_code == 403
