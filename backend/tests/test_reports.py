import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def _create_listing(client, token) -> str:
    listing = await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "ELECTRONICS",
            "title": "Report Target Item",
            "description": "desc",
            "price": 10000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(token),
    )
    return listing.json()["data"]["id"]


async def _make_admin(db, email: str) -> None:
    await db.users.update_one({"email": email}, {"$set": {"roles": ["ADMIN"]}})


async def test_report_listing(client):
    owner_token = await signup_and_login(client, "reportowner@example.com", "ReportOwner")
    reporter_token = await signup_and_login(client, "reporter@example.com", "Reporter")
    listing_id = await _create_listing(client, owner_token)

    response = await client.post(
        "/api/v1/reports",
        json={"target_type": "MARKETPLACE", "target_id": listing_id, "reason": "SCAM", "details": "looks fake"},
        headers=auth_headers(reporter_token),
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["status"] == "PENDING"
    assert data["reporter"]["name"] == "Reporter"


async def test_report_nonexistent_target_returns_404(client):
    reporter_token = await signup_and_login(client, "reporter2@example.com", "Reporter2")
    response = await client.post(
        "/api/v1/reports",
        json={"target_type": "MARKETPLACE", "target_id": "64a000000000000000000000", "reason": "SPAM"},
        headers=auth_headers(reporter_token),
    )
    assert response.status_code == 404


async def test_report_self_rejected(client):
    token = await signup_and_login(client, "selfreporter@example.com", "SelfReporter")
    me = await client.get("/api/v1/users/me", headers=auth_headers(token))
    user_id = me.json()["data"]["id"]

    response = await client.post(
        "/api/v1/reports",
        json={"target_type": "USER", "target_id": user_id, "reason": "OTHER"},
        headers=auth_headers(token),
    )
    assert response.status_code == 422


async def test_reports_require_auth(client):
    response = await client.post(
        "/api/v1/reports", json={"target_type": "MARKETPLACE", "target_id": "64a000000000000000000000", "reason": "SPAM"}
    )
    assert response.status_code == 401


async def test_non_admin_cannot_list_or_resolve_reports(client):
    owner_token = await signup_and_login(client, "noadmin-owner@example.com", "NoAdminOwner")
    reporter_token = await signup_and_login(client, "noadmin-reporter@example.com", "NoAdminReporter")
    listing_id = await _create_listing(client, owner_token)
    await client.post(
        "/api/v1/reports",
        json={"target_type": "MARKETPLACE", "target_id": listing_id, "reason": "SPAM"},
        headers=auth_headers(reporter_token),
    )

    list_response = await client.get("/api/v1/reports", headers=auth_headers(reporter_token))
    assert list_response.status_code == 403


async def test_admin_can_list_and_resolve_reports(client, db):
    owner_token = await signup_and_login(client, "adminflow-owner@example.com", "AdminFlowOwner")
    reporter_token = await signup_and_login(client, "adminflow-reporter@example.com", "AdminFlowReporter")
    admin_token = await signup_and_login(client, "admin1@example.com", "Admin1")
    await _make_admin(db, "admin1@example.com")

    listing_id = await _create_listing(client, owner_token)
    create = await client.post(
        "/api/v1/reports",
        json={"target_type": "MARKETPLACE", "target_id": listing_id, "reason": "FAKE_LISTING"},
        headers=auth_headers(reporter_token),
    )
    report_id = create.json()["data"]["id"]

    listed = await client.get("/api/v1/reports?status=PENDING", headers=auth_headers(admin_token))
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 1

    resolved = await client.post(
        f"/api/v1/reports/{report_id}/resolve",
        json={"status": "RESOLVED"},
        headers=auth_headers(admin_token),
    )
    assert resolved.status_code == 200
    assert resolved.json()["data"]["status"] == "RESOLVED"

    remaining_pending = await client.get("/api/v1/reports?status=PENDING", headers=auth_headers(admin_token))
    assert remaining_pending.json()["data"]["total"] == 0
