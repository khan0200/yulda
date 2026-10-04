import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def _get_user_id(client, token) -> str:
    me = await client.get("/api/v1/auth/me", headers=auth_headers(token))
    return me.json()["data"]["id"]


async def test_start_conversation_and_send_message(client):
    alice_token = await signup_and_login(client, "alice@example.com", "Alice")
    bob_token = await signup_and_login(client, "bob@example.com", "Bob")
    bob_id = await _get_user_id(client, bob_token)

    start = await client.post(
        "/api/v1/conversations",
        json={"target_user_id": bob_id, "listing_type": "MARKETPLACE", "listing_id": "abc123", "listing_title": "iPhone"},
        headers=auth_headers(alice_token),
    )
    assert start.status_code == 201
    convo = start.json()["data"]
    assert convo["listing_title"] == "iPhone"
    assert len(convo["participants"]) == 2
    convo_id = convo["id"]

    send = await client.post(
        f"/api/v1/conversations/{convo_id}/messages",
        json={"body": "Is this still available?"},
        headers=auth_headers(alice_token),
    )
    assert send.status_code == 201
    assert send.json()["data"]["body"] == "Is this still available?"

    messages = await client.get(f"/api/v1/conversations/{convo_id}/messages", headers=auth_headers(bob_token))
    assert messages.status_code == 200
    assert messages.json()["data"]["total"] == 1


async def test_starting_conversation_twice_reuses_existing(client):
    alice_token = await signup_and_login(client, "alice2@example.com", "Alice2")
    bob_token = await signup_and_login(client, "bob2@example.com", "Bob2")
    bob_id = await _get_user_id(client, bob_token)

    first = await client.post(
        "/api/v1/conversations",
        json={"target_user_id": bob_id, "listing_id": "xyz"},
        headers=auth_headers(alice_token),
    )
    second = await client.post(
        "/api/v1/conversations",
        json={"target_user_id": bob_id, "listing_id": "xyz"},
        headers=auth_headers(alice_token),
    )
    assert first.json()["data"]["id"] == second.json()["data"]["id"]


async def test_cannot_message_yourself(client):
    token = await signup_and_login(client, "solo@example.com", "Solo")
    user_id = await _get_user_id(client, token)
    response = await client.post(
        "/api/v1/conversations", json={"target_user_id": user_id}, headers=auth_headers(token)
    )
    assert response.status_code == 422


async def test_non_participant_cannot_read_or_send(client):
    alice_token = await signup_and_login(client, "alice3@example.com", "Alice3")
    bob_token = await signup_and_login(client, "bob3@example.com", "Bob3")
    stranger_token = await signup_and_login(client, "stranger3@example.com", "Stranger3")
    bob_id = await _get_user_id(client, bob_token)

    start = await client.post(
        "/api/v1/conversations", json={"target_user_id": bob_id}, headers=auth_headers(alice_token)
    )
    convo_id = start.json()["data"]["id"]

    forbidden_read = await client.get(
        f"/api/v1/conversations/{convo_id}/messages", headers=auth_headers(stranger_token)
    )
    assert forbidden_read.status_code == 403

    forbidden_send = await client.post(
        f"/api/v1/conversations/{convo_id}/messages",
        json={"body": "hi"},
        headers=auth_headers(stranger_token),
    )
    assert forbidden_send.status_code == 403


async def test_list_my_conversations_and_unread_count(client):
    alice_token = await signup_and_login(client, "alice4@example.com", "Alice4")
    bob_token = await signup_and_login(client, "bob4@example.com", "Bob4")
    bob_id = await _get_user_id(client, bob_token)

    start = await client.post(
        "/api/v1/conversations", json={"target_user_id": bob_id}, headers=auth_headers(alice_token)
    )
    convo_id = start.json()["data"]["id"]

    await client.post(
        f"/api/v1/conversations/{convo_id}/messages", json={"body": "hello"}, headers=auth_headers(alice_token)
    )

    bob_list = await client.get("/api/v1/conversations", headers=auth_headers(bob_token))
    assert bob_list.status_code == 200
    bob_convo = next(c for c in bob_list.json()["data"]["items"] if c["id"] == convo_id)
    assert bob_convo["unread_count"] == 1
    assert bob_convo["last_message_preview"] == "hello"

    mark_read = await client.post(f"/api/v1/conversations/{convo_id}/read", headers=auth_headers(bob_token))
    assert mark_read.status_code == 200

    bob_list_after = await client.get("/api/v1/conversations", headers=auth_headers(bob_token))
    bob_convo_after = next(c for c in bob_list_after.json()["data"]["items"] if c["id"] == convo_id)
    assert bob_convo_after["unread_count"] == 0


async def test_new_message_creates_notification_for_recipient(client):
    alice_token = await signup_and_login(client, "alice5@example.com", "Alice5")
    bob_token = await signup_and_login(client, "bob5@example.com", "Bob5")
    bob_id = await _get_user_id(client, bob_token)

    start = await client.post(
        "/api/v1/conversations", json={"target_user_id": bob_id}, headers=auth_headers(alice_token)
    )
    convo_id = start.json()["data"]["id"]

    await client.post(
        f"/api/v1/conversations/{convo_id}/messages", json={"body": "hey there"}, headers=auth_headers(alice_token)
    )

    notifications = await client.get("/api/v1/notifications", headers=auth_headers(bob_token))
    assert notifications.status_code == 200
    items = notifications.json()["data"]["items"]
    assert any(n["type"] == "NEW_MESSAGE" and n["title"] == "Alice5" for n in items)

    unread = await client.get("/api/v1/notifications/unread-count", headers=auth_headers(bob_token))
    assert unread.json()["data"]["unread_count"] == 1
