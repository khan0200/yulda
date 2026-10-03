import pytest

from tests.conftest import auth_headers, signup_and_login

pytestmark = pytest.mark.asyncio


async def test_presign_requires_auth(client):
    response = await client.post(
        "/api/v1/uploads/presign",
        json={"filename": "car.jpg", "content_type": "image/jpeg", "folder": "auto"},
    )
    assert response.status_code == 401


async def test_presign_returns_upload_and_public_url(client):
    token = await signup_and_login(client, "uploader@example.com", "Uploader")
    response = await client.post(
        "/api/v1/uploads/presign",
        json={"filename": "car.jpg", "content_type": "image/jpeg", "folder": "auto"},
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["upload_url"].startswith("http")
    assert data["public_url"].startswith("http")
    assert "auto/" in data["public_url"]
    assert data["public_url"].endswith(".jpg")


async def test_presign_rejects_disallowed_content_type(client):
    token = await signup_and_login(client, "baduploader@example.com", "BadUploader")
    response = await client.post(
        "/api/v1/uploads/presign",
        json={"filename": "script.exe", "content_type": "application/x-msdownload", "folder": "auto"},
        headers=auth_headers(token),
    )
    assert response.status_code == 422


async def test_presign_rejects_disallowed_extension(client):
    token = await signup_and_login(client, "mismatcheduploader@example.com", "Mismatched")
    response = await client.post(
        "/api/v1/uploads/presign",
        # image content-type but a non-image filename extension
        json={"filename": "notes.txt", "content_type": "image/jpeg", "folder": "marketplace"},
        headers=auth_headers(token),
    )
    assert response.status_code == 422


async def test_presign_rejects_invalid_folder(client):
    token = await signup_and_login(client, "folderuploader@example.com", "FolderUploader")
    response = await client.post(
        "/api/v1/uploads/presign",
        json={"filename": "car.jpg", "content_type": "image/jpeg", "folder": "not-a-real-folder"},
        headers=auth_headers(token),
    )
    assert response.status_code == 422


async def test_presign_generates_unique_keys_for_same_filename(client):
    token = await signup_and_login(client, "uniqueuploader@example.com", "UniqueUploader")
    first = await client.post(
        "/api/v1/uploads/presign",
        json={"filename": "photo.png", "content_type": "image/png", "folder": "housing"},
        headers=auth_headers(token),
    )
    second = await client.post(
        "/api/v1/uploads/presign",
        json={"filename": "photo.png", "content_type": "image/png", "folder": "housing"},
        headers=auth_headers(token),
    )
    assert first.json()["data"]["public_url"] != second.json()["data"]["public_url"]
