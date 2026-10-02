import pytest

pytestmark = pytest.mark.asyncio


async def _signup_and_login(client, email: str, name: str) -> str:
    await client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": "StrongPass123", "name": name},
    )
    login = await client.post("/api/v1/auth/login", json={"email": email, "password": "StrongPass123"})
    return login.json()["data"]["access_token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


async def test_create_and_get_post(client):
    token = await _signup_and_login(client, "poster@example.com", "Poster")
    response = await client.post(
        "/api/v1/community/posts",
        json={"category": "QUESTION", "title": "Dongdemunda suitlar bormi?", "body": "Kimdir biladimi?"},
        headers=_auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["title"] == "Dongdemunda suitlar bormi?"
    assert body["author"]["name"] == "Poster"
    assert body["comment_count"] == 0

    post_id = body["id"]
    get_response = await client.get(f"/api/v1/community/posts/{post_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["title"] == "Dongdemunda suitlar bormi?"


async def test_create_post_requires_auth(client):
    response = await client.post(
        "/api/v1/community/posts",
        json={"category": "QUESTION", "title": "Test", "body": "Test body"},
    )
    assert response.status_code == 401


async def test_list_posts_filters_by_category(client):
    token = await _signup_and_login(client, "filter@example.com", "Filter User")
    await client.post(
        "/api/v1/community/posts",
        json={"category": "QUESTION", "title": "Q1", "body": "body"},
        headers=_auth_headers(token),
    )
    await client.post(
        "/api/v1/community/posts",
        json={"category": "MEETUP", "title": "M1", "body": "body"},
        headers=_auth_headers(token),
    )

    response = await client.get("/api/v1/community/posts", params={"category": "MEETUP"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["title"] == "M1"


async def test_add_and_list_comments(client):
    token = await _signup_and_login(client, "commenter@example.com", "Commenter")
    post_response = await client.post(
        "/api/v1/community/posts",
        json={"category": "LOST_AND_FOUND", "title": "Lost wallet", "body": "Near the library"},
        headers=_auth_headers(token),
    )
    post_id = post_response.json()["data"]["id"]

    comment_response = await client.post(
        f"/api/v1/community/posts/{post_id}/comments",
        json={"body": "I found it, DM me"},
        headers=_auth_headers(token),
    )
    assert comment_response.status_code == 201
    assert comment_response.json()["data"]["body"] == "I found it, DM me"

    post_after = await client.get(f"/api/v1/community/posts/{post_id}")
    assert post_after.json()["data"]["comment_count"] == 1

    comments = await client.get(f"/api/v1/community/posts/{post_id}/comments")
    assert comments.json()["data"]["total"] == 1


async def test_only_author_can_delete_post(client):
    author_token = await _signup_and_login(client, "author@example.com", "Author")
    other_token = await _signup_and_login(client, "other@example.com", "Other")

    post_response = await client.post(
        "/api/v1/community/posts",
        json={"category": "OTHER", "title": "My post", "body": "body"},
        headers=_auth_headers(author_token),
    )
    post_id = post_response.json()["data"]["id"]

    forbidden = await client.delete(f"/api/v1/community/posts/{post_id}", headers=_auth_headers(other_token))
    assert forbidden.status_code == 403

    allowed = await client.delete(f"/api/v1/community/posts/{post_id}", headers=_auth_headers(author_token))
    assert allowed.status_code == 200

    gone = await client.get(f"/api/v1/community/posts/{post_id}")
    assert gone.status_code == 404


async def test_get_nonexistent_post_returns_404(client):
    response = await client.get("/api/v1/community/posts/000000000000000000000000")
    assert response.status_code == 404
