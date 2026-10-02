import pytest

pytestmark = pytest.mark.asyncio


async def test_signup_creates_user_and_returns_tokens(client):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "rider@example.com", "password": "StrongPass123", "name": "Rider One"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert "refresh_token" in body["data"]


async def test_signup_rejects_duplicate_email(client):
    payload = {"email": "dup@example.com", "password": "StrongPass123", "name": "Dup User"}
    await client.post("/api/v1/auth/signup", json=payload)
    response = await client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 409
    assert response.json()["error_code"] == "CONFLICT"


async def test_signup_rejects_admin_self_assignment(client):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "hacker@example.com", "password": "StrongPass123", "name": "Hacker", "roles": ["ADMIN"]},
    )
    assert response.status_code == 422


async def test_login_and_me_flow(client):
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "login@example.com", "password": "StrongPass123", "name": "Login User"},
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "StrongPass123"},
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["data"]["access_token"]

    me_response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me_response.status_code == 200
    assert me_response.json()["data"]["email"] == "login@example.com"
    assert "password_hash" not in me_response.json()["data"]


async def test_login_rejects_wrong_password(client):
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "wrong@example.com", "password": "StrongPass123", "name": "Wrong Pass"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "BadPassword1"},
    )
    assert response.status_code == 401


async def test_protected_route_requires_token(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


async def test_refresh_token_flow(client):
    signup = await client.post(
        "/api/v1/auth/signup",
        json={"email": "refresh@example.com", "password": "StrongPass123", "name": "Refresh User"},
    )
    refresh_token = signup.json()["data"]["refresh_token"]
    response = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]
