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


async def test_create_job_post_defaults_to_phone_contact(client):
    token = await signup_and_login(client, "phonedefault@example.com", "PhoneDefault")
    response = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "RETAIL",
            "employment_type": "PART_TIME",
            "title": "Default contact method",
            "description": "desc",
            "contact_value": "010-1111-9999",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["contact_method"] == "PHONE"
    assert body["contact_value"] == "010-1111-9999"


async def test_create_job_post_with_chat_contact_method(client):
    token = await signup_and_login(client, "chatcontact@example.com", "ChatContact")
    response = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "RETAIL",
            "employment_type": "PART_TIME",
            "title": "Message only contact",
            "description": "desc",
            "contact_method": "CHAT",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["contact_method"] == "CHAT"
    assert body["contact_value"] is None


async def test_create_job_post_phone_method_without_value_rejected(client):
    token = await signup_and_login(client, "phonemissing@example.com", "PhoneMissing")
    response = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "RETAIL",
            "employment_type": "PART_TIME",
            "title": "Missing phone",
            "description": "desc",
            "contact_method": "PHONE",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 422


async def test_create_job_post_with_visa_housing_overtime(client):
    token = await signup_and_login(client, "visajob@example.com", "VisaJob")
    response = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "CONSTRUCTION_FACTORY",
            "employment_type": "FULL_TIME",
            "title": "Factory packing work",
            "description": "desc",
            "pay_type": "MONTHLY",
            "pay_amount": 2400000,
            "overtime_pay_amount": 12000,
            "accepted_visas": ["H2", "F4", "F5"],
            "housing_option": "PROVIDED_PAID",
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["overtime_pay_amount"] == 12000
    assert set(body["accepted_visas"]) == {"H2", "F4", "F5"}
    assert body["housing_option"] == "PROVIDED_PAID"


async def test_job_post_defaults_for_visa_and_housing(client):
    token = await signup_and_login(client, "defaultvisa@example.com", "DefaultVisa")
    response = await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "RETAIL",
            "employment_type": "PART_TIME",
            "title": "No visa info given",
            "description": "desc",
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )
    body = response.json()["data"]
    assert body["accepted_visas"] == []
    assert body["housing_option"] == "NOT_PROVIDED"
    assert body["overtime_pay_amount"] is None


async def test_filter_jobs_by_accepted_visa(client):
    token = await signup_and_login(client, "visafilter@example.com", "VisaFilter")
    await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "CONSTRUCTION_FACTORY",
            "employment_type": "FULL_TIME",
            "title": "D2 friendly job",
            "description": "desc",
            "accepted_visas": ["D2", "G1"],
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )
    await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "CONSTRUCTION_FACTORY",
            "employment_type": "FULL_TIME",
            "title": "E9 only job",
            "description": "desc",
            "accepted_visas": ["E9"],
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )

    response = await client.get("/api/v1/jobs/posts", params={"accepted_visa": "D2"})
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["title"] == "D2 friendly job"


async def test_filter_jobs_by_housing_option(client):
    token = await signup_and_login(client, "housingfilter@example.com", "HousingFilter")
    await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "CONSTRUCTION_FACTORY",
            "employment_type": "FULL_TIME",
            "title": "Free dorm job",
            "description": "desc",
            "housing_option": "PROVIDED_FREE",
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )
    await client.post(
        "/api/v1/jobs/posts",
        json={
            "post_type": "OFFER",
            "category": "CONSTRUCTION_FACTORY",
            "employment_type": "FULL_TIME",
            "title": "No housing job",
            "description": "desc",
            "contact_value": "010-1111-2222",
        },
        headers=auth_headers(token),
    )

    response = await client.get("/api/v1/jobs/posts", params={"housing_option": "PROVIDED_FREE"})
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Free dorm job"


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
