import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def _user_id(client, token) -> str:
    me = await client.get("/api/v1/users/me", headers=auth_headers(token))
    return me.json()["data"]["id"]


async def test_block_and_list(client):
    blocker_token = await signup_and_login(client, "blocker@example.com", "Blocker")
    blocked_token = await signup_and_login(client, "blocked@example.com", "Blocked")
    blocked_id = await _user_id(client, blocked_token)

    response = await client.post(
        "/api/v1/blocks", json={"blocked_user_id": blocked_id}, headers=auth_headers(blocker_token)
    )
    assert response.status_code == 201
    assert response.json()["data"]["blocked_user"]["name"] == "Blocked"

    listed = await client.get("/api/v1/blocks", headers=auth_headers(blocker_token))
    assert len(listed.json()["data"]) == 1


async def test_block_is_idempotent(client):
    blocker_token = await signup_and_login(client, "idemblocker@example.com", "IdemBlocker")
    blocked_token = await signup_and_login(client, "idemblocked@example.com", "IdemBlocked")
    blocked_id = await _user_id(client, blocked_token)

    await client.post("/api/v1/blocks", json={"blocked_user_id": blocked_id}, headers=auth_headers(blocker_token))
    second = await client.post(
        "/api/v1/blocks", json={"blocked_user_id": blocked_id}, headers=auth_headers(blocker_token)
    )
    assert second.status_code == 201

    listed = await client.get("/api/v1/blocks", headers=auth_headers(blocker_token))
    assert len(listed.json()["data"]) == 1


async def test_cannot_block_self(client):
    token = await signup_and_login(client, "selfblocker@example.com", "SelfBlocker")
    user_id = await _user_id(client, token)

    response = await client.post("/api/v1/blocks", json={"blocked_user_id": user_id}, headers=auth_headers(token))
    assert response.status_code == 422


async def test_unblock(client):
    blocker_token = await signup_and_login(client, "unblocker@example.com", "Unblocker")
    blocked_token = await signup_and_login(client, "unblocked@example.com", "Unblocked")
    blocked_id = await _user_id(client, blocked_token)

    await client.post("/api/v1/blocks", json={"blocked_user_id": blocked_id}, headers=auth_headers(blocker_token))
    unblock = await client.delete(f"/api/v1/blocks/{blocked_id}", headers=auth_headers(blocker_token))
    assert unblock.status_code == 200

    listed = await client.get("/api/v1/blocks", headers=auth_headers(blocker_token))
    assert len(listed.json()["data"]) == 0


async def test_blocked_user_cannot_start_conversation(client):
    blocker_token = await signup_and_login(client, "convblocker@example.com", "ConvBlocker")
    blocked_token = await signup_and_login(client, "convblocked@example.com", "ConvBlocked")
    blocker_id = await _user_id(client, blocker_token)
    blocked_id = await _user_id(client, blocked_token)

    await client.post("/api/v1/blocks", json={"blocked_user_id": blocked_id}, headers=auth_headers(blocker_token))

    response = await client.post(
        "/api/v1/conversations", json={"target_user_id": blocker_id}, headers=auth_headers(blocked_token)
    )
    assert response.status_code == 403


async def test_blocking_after_conversation_prevents_further_messages(client):
    blocker_token = await signup_and_login(client, "midblocker@example.com", "MidBlocker")
    blocked_token = await signup_and_login(client, "midblocked@example.com", "MidBlocked")
    blocked_id = await _user_id(client, blocked_token)

    convo = await client.post(
        "/api/v1/conversations", json={"target_user_id": blocked_id}, headers=auth_headers(blocker_token)
    )
    conversation_id = convo.json()["data"]["id"]

    await client.post("/api/v1/blocks", json={"blocked_user_id": blocked_id}, headers=auth_headers(blocker_token))

    send = await client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"body": "hello"},
        headers=auth_headers(blocked_token),
    )
    assert send.status_code == 403


async def test_blocks_require_auth(client):
    response = await client.get("/api/v1/blocks")
    assert response.status_code == 401
