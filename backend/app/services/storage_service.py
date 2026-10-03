import uuid

import boto3
from botocore.client import Config as BotoConfig

from app.core.config import settings

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
PRESIGNED_URL_EXPIRY_SECONDS = 300


class StorageService:
    def __init__(self) -> None:
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.STORAGE_ENDPOINT,
            aws_access_key_id=settings.STORAGE_ACCESS_KEY,
            aws_secret_access_key=settings.STORAGE_SECRET_KEY,
            region_name=settings.STORAGE_REGION,
            config=BotoConfig(signature_version="s3v4"),
        )

    def build_object_key(self, folder: str, filename: str) -> str:
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {extension}")
        unique_name = f"{uuid.uuid4().hex}.{extension}"
        return f"{folder}/{unique_name}"

    def create_presigned_upload(self, object_key: str, content_type: str) -> dict[str, str]:
        upload_url = self._client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.STORAGE_BUCKET,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=PRESIGNED_URL_EXPIRY_SECONDS,
        )
        public_url = f"{settings.STORAGE_PUBLIC_BASE_URL}/{object_key}"
        return {"upload_url": upload_url, "public_url": public_url}


_storage_service: StorageService | None = None


def get_storage_service() -> StorageService:
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service
