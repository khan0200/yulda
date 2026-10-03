import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def test_create_and_get_job_offer(client):
    token = await signup_and_login(client, "employer@example.com", "Employer")
    response = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "RESTAURANT_CAFE",
            "employment_type": "PART_TIME",
            "title": "Kitchen helper needed",
            "description": "Evening shifts, no experience required",
            "pay_type": "HOURLY",
            "pay_amount": 11000,
            "city": "Ansan",
            "requires_korean": False,
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["title"] == "Kitchen helper needed"
    assert body["post_type"] == "OFFER"
    assert body["status"] == "ACTIVE"
    assert body["owner"]["name"] == "Employer"
    assert body["like_count"] == 0

    job_id = body["id"]
    get_response = await client.get(f"/api/v1/jobs/posts/{job_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["pay_amount"] == 11000


async def test_create_job_post_requires_auth(client):
    response = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "REQUEST",
            "category": "DELIVERY_LOGISTICS",
            "employment_type": "DAILY",
            "title": "Looking for delivery work",
            "description": "Available weekends",
            "contact_value": "010-0000-0000",
        },
    )
    assert response.status_code == 401


async def test_list_jobs_filters_by_post_type_and_category(client):
    token = await signup_and_login(client, "jobposter@example.com", "JobPoster")
    await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "RETAIL",
            "employment_type": "FULL_TIME",
            "title": "Store clerk",
            "description": "desc",
            "contact_value": "010-1234-5678",
        },
        headers=auth_headers(token),
    )
    await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "REQUEST",
            "category": "RETAIL",
            "employment_type": "FULL_TIME",
            "title": "Looking for retail work",
            "description": "desc",
            "contact_value": "010-1234-5678",
        },
        headers=auth_headers(token),
    )

    response = await client.get("/api/v1/jobs/posts", params={"post_type": "OFFER", "category": "RETAIL"})
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Store clerk"


async def test_only_owner_can_delete_job_post(client):
    owner_token = await signup_and_login(client, "jobowner@example.com", "JobOwner")
    other_token = await signup_and_login(client, "jobstranger@example.com", "JobStranger")

    create = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "CLEANING",
            "employment_type": "PART_TIME",
            "title": "Cleaner needed",
            "description": "desc",
            "contact_value": "010-9999-0000",
        },
        headers=auth_headers(owner_token),
    )
    job_id = create.json()["data"]["id"]

    forbidden = await client.delete(f"/api/v1/jobs/posts/{job_id}", headers=auth_headers(other_token))
    assert forbidden.status_code == 403

    allowed = await client.delete(f"/api/v1/jobs/posts/{job_id}", headers=auth_headers(owner_token))
    assert allowed.status_code == 200

    gone = await client.get(f"/api/v1/jobs/posts/{job_id}")
    assert gone.status_code == 404


async def test_toggle_favorite_on_job_post(client):
    owner_token = await signup_and_login(client, "jobowner2@example.com", "JobOwner2")
    liker_token = await signup_and_login(client, "jobliker@example.com", "JobLiker")

    create = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "IT_DESIGN",
            "employment_type": "CONTRACT",
            "title": "Frontend contractor",
            "description": "desc",
            "contact_value": "010-5555-5555",
        },
        headers=auth_headers(owner_token),
    )
    job_id = create.json()["data"]["id"]

    like = await client.post(f"/api/v1/favorites/JOBS/{job_id}/toggle", headers=auth_headers(liker_token))
    assert like.status_code == 200
    assert like.json()["data"]["like_count"] == 1

    get_post = await client.get(f"/api/v1/jobs/posts/{job_id}")
    assert get_post.json()["data"]["like_count"] == 1
