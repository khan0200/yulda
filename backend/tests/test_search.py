import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def test_search_returns_matching_marketplace_and_community_results(client):
    token = await signup_and_login(client, "searcher@example.com", "Searcher")

    await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "ELECTRONICS",
            "title": "Vintage Camera for sale",
            "description": "Works great",
            "price": 80000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(token),
    )
    await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "FURNITURE",
            "title": "Sofa for sale",
            "description": "desc",
            "price": 50000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(token),
    )
    await client.post(
        "/api/v1/community/posts",
        json={"category": "QUESTION", "title": "Where to buy a camera lens?", "body": "Looking for recommendations"},
        headers=auth_headers(token),
    )

    response = await client.get("/api/v1/search", params={"q": "camera"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["marketplace"]) == 1
    assert data["marketplace"][0]["title"] == "Vintage Camera for sale"
    assert len(data["community"]) == 1
    assert data["community"][0]["title"] == "Where to buy a camera lens?"


async def test_search_is_case_insensitive_and_empty_for_no_match(client):
    token = await signup_and_login(client, "searcher2@example.com", "Searcher2")
    await client.post(
        "/api/v1/marketplace/listings",
        json={
            "category": "ELECTRONICS",
            "title": "MacBook Pro",
            "description": "desc",
            "price": 1000000,
            "condition": "USED",
            "contact_method": "CHAT",
            "contact_value": "chat-id",
        },
        headers=auth_headers(token),
    )

    response = await client.get("/api/v1/search", params={"q": "macbook"})
    assert response.json()["data"]["marketplace"][0]["title"] == "MacBook Pro"

    no_match = await client.get("/api/v1/search", params={"q": "nonexistentxyz123"})
    assert no_match.json()["data"]["marketplace"] == []
    assert no_match.json()["data"]["community"] == []


async def test_search_requires_query_param(client):
    response = await client.get("/api/v1/search")
    assert response.status_code == 422
