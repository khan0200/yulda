import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def test_update_my_profile(client):
    token = await signup_and_login(client, "profileuser@example.com", "Profile User")
    response = await client.patch(
        "/api/v1/users/me",
        json={"name": "Updated Name", "phone": "010-1111-2222"},
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["name"] == "Updated Name"
    assert body["phone"] == "010-1111-2222"


async def test_change_password_success_and_relogin(client):
    token = await signup_and_login(client, "pwchange@example.com", "PW Change")
    response = await client.post(
        "/api/v1/users/me/change-password",
        json={"current_password": "StrongPass123", "new_password": "NewStrongPass456"},
        headers=auth_headers(token),
    )
    assert response.status_code == 200

    old_login = await client.post(
        "/api/v1/auth/login", json={"email": "pwchange@example.com", "password": "StrongPass123"}
    )
    assert old_login.status_code == 401

    new_login = await client.post(
        "/api/v1/auth/login", json={"email": "pwchange@example.com", "password": "NewStrongPass456"}
    )
    assert new_login.status_code == 200


async def test_change_password_rejects_wrong_current_password(client):
    token = await signup_and_login(client, "pwfail@example.com", "PW Fail")
    response = await client.post(
        "/api/v1/users/me/change-password",
        json={"current_password": "WrongPassword1", "new_password": "NewStrongPass456"},
        headers=auth_headers(token),
    )
    assert response.status_code == 422


async def test_change_password_requires_auth(client):
    response = await client.post(
        "/api/v1/users/me/change-password",
        json={"current_password": "x", "new_password": "NewStrongPass456"},
    )
    assert response.status_code == 401


async def test_delete_account_requires_correct_password(client):
    token = await signup_and_login(client, "delwrongpw@example.com", "DelWrongPw")
    response = await client.request(
        "DELETE", "/api/v1/users/me", json={"password": "WrongPassword1"}, headers=auth_headers(token)
    )
    assert response.status_code == 422


async def test_delete_account_success(client):
    token = await signup_and_login(client, "deluser@example.com", "DelUser")
    response = await client.request(
        "DELETE", "/api/v1/users/me", json={"password": "StrongPass123"}, headers=auth_headers(token)
    )
    assert response.status_code == 200

    me = await client.get("/api/v1/users/me", headers=auth_headers(token))
    assert me.status_code == 401

    login_again = await client.post(
        "/api/v1/auth/login", json={"email": "deluser@example.com", "password": "StrongPass123"}
    )
    assert login_again.status_code == 401


async def test_delete_account_requires_auth(client):
    response = await client.request("DELETE", "/api/v1/users/me", json={"password": "x"})
    assert response.status_code == 401
