import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


MARKETPLACE_PAYLOAD = {
    "category": "ELECTRONICS",
    "title": "My Laptop",
    "description": "desc",
    "price": 500000,
    "condition": "USED",
    "contact_method": "CHAT",
    "contact_value": "chat-id",
}

HOUSING_PAYLOAD = {
    "housing_type": "ONE_ROOM",
    "title": "My Room",
    "description": "desc",
    "deposit": 1000000,
    "monthly_rent": 400000,
    "contact_value": "010-1111-2222",
}

AUTO_PAYLOAD = {
    "listing_type": "SALE",
    "make": "Hyundai",
    "model": "Avante",
    "year": 2020,
    "mileage_km": 50000,
    "fuel_type": "GASOLINE",
    "transmission": "AUTOMATIC",
    "price": 15000000,
    "description": "desc",
    "contact_value": "010-1111-2222",
}

JOB_PAYLOAD = {
    "post_type": "OFFER",
    "category": "RESTAURANT_CAFE",
    "employment_type": "PART_TIME",
    "title": "Helper needed",
    "description": "desc",
    "contact_value": "010-1111-2222",
}

SERVICE_PAYLOAD = {
    "category": "BEAUTY",
    "title": "Haircut",
    "description": "desc",
    "contact_value": "010-1111-2222",
}


@pytest.mark.parametrize(
    "prefix,payload,status_field,status_values",
    [
        ("marketplace/listings", MARKETPLACE_PAYLOAD, "status", ("PAUSED", "ACTIVE")),
        ("housing/listings", HOUSING_PAYLOAD, "status", ("PAUSED", "ACTIVE")),
        ("auto/listings", AUTO_PAYLOAD, "status", ("UNAVAILABLE", "ACTIVE")),
        ("jobs/posts", JOB_PAYLOAD, "status", ("CLOSED", "ACTIVE")),
        ("services/posts", SERVICE_PAYLOAD, "status", ("UNAVAILABLE", "ACTIVE")),
    ],
)
async def test_my_listings_lifecycle(client, prefix, payload, status_field, status_values):
    owner_token = await signup_and_login(client, f"owner-{prefix.replace('/', '-')}@example.com", "Owner")
    other_token = await signup_and_login(client, f"other-{prefix.replace('/', '-')}@example.com", "Other")

    create = await client.post(f"/api/v1/{prefix}", json=payload, headers=auth_headers(owner_token))
    assert create.status_code == 201
    item_id = create.json()["data"]["id"]
    original_created_at = create.json()["data"]["created_at"]

    mine = await client.get(f"/api/v1/{prefix}/mine", headers=auth_headers(owner_token))
    assert mine.status_code == 200
    assert any(i["id"] == item_id for i in mine.json()["data"]["items"])

    other_mine = await client.get(f"/api/v1/{prefix}/mine", headers=auth_headers(other_token))
    assert not any(i["id"] == item_id for i in other_mine.json()["data"]["items"])

    deactivated_status, reactivated_status = status_values
    deactivate = await client.patch(
        f"/api/v1/{prefix}/{item_id}", json={status_field: deactivated_status}, headers=auth_headers(owner_token)
    )
    assert deactivate.status_code == 200
    assert deactivate.json()["data"][status_field] == deactivated_status

    mine_after_deactivate = await client.get(f"/api/v1/{prefix}/mine", headers=auth_headers(owner_token))
    assert any(i["id"] == item_id for i in mine_after_deactivate.json()["data"]["items"])

    repost = await client.post(f"/api/v1/{prefix}/{item_id}/repost", headers=auth_headers(owner_token))
    assert repost.status_code == 200
    repost_body = repost.json()["data"]
    assert repost_body[status_field] == reactivated_status
    assert repost_body["created_at"] != original_created_at

    forbidden_repost = await client.post(f"/api/v1/{prefix}/{item_id}/repost", headers=auth_headers(other_token))
    assert forbidden_repost.status_code == 403

    delete = await client.delete(f"/api/v1/{prefix}/{item_id}", headers=auth_headers(owner_token))
    assert delete.status_code == 200
