import pytest

pytestmark = pytest.mark.asyncio


async def test_login_sets_auth_cookies(client):
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "cookieuser@example.com", "password": "StrongPass123", "name": "Cookie User"},
    )
    response = await client.post(
        "/api/v1/auth/login", json={"email": "cookieuser@example.com", "password": "StrongPass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


async def test_cookie_alone_authenticates_request(client):
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "cookieonly@example.com", "password": "StrongPass123", "name": "Cookie Only"},
    )
    await client.post("/api/v1/auth/login", json={"email": "cookieonly@example.com", "password": "StrongPass123"})

    me = await client.get("/api/v1/users/me")
    assert me.status_code == 200
    assert me.json()["data"]["email"] == "cookieonly@example.com"


async def test_refresh_via_cookie_with_no_body(client):
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "cookierefresh@example.com", "password": "StrongPass123", "name": "Cookie Refresh"},
    )
    await client.post(
        "/api/v1/auth/login", json={"email": "cookierefresh@example.com", "password": "StrongPass123"}
    )

    refresh = await client.post("/api/v1/auth/refresh")
    assert refresh.status_code == 200
    assert "access_token" in refresh.cookies


async def test_logout_clears_cookies(client):
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "cookielogout@example.com", "password": "StrongPass123", "name": "Cookie Logout"},
    )
    await client.post("/api/v1/auth/login", json={"email": "cookielogout@example.com", "password": "StrongPass123"})

    logout = await client.post("/api/v1/auth/logout")
    assert logout.status_code == 200

    me = await client.get("/api/v1/users/me")
    assert me.status_code == 401


async def test_bearer_header_still_works_without_cookies(client):
    signup = await client.post(
        "/api/v1/auth/signup",
        json={"email": "bearerstill@example.com", "password": "StrongPass123", "name": "Bearer Still"},
    )
    token = signup.json()["data"]["access_token"]
    client.cookies.clear()

    me = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
