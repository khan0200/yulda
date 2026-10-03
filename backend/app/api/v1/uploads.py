from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.exceptions import ValidationError
from app.core.responses import ApiResponse
from app.schemas.upload import PresignUploadRequest, PresignUploadResponse
from app.services.storage_service import (
    ALLOWED_IMAGE_EXTENSIONS,
    StorageService,
    get_storage_service,
)

router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": {"jpg", "jpeg"},
    "image/png": {"png"},
    "image/webp": {"webp"},
}


@router.post("/presign", response_model=ApiResponse[PresignUploadResponse])
async def presign_upload(
    payload: PresignUploadRequest,
    user: dict = Depends(get_current_user),
    storage: StorageService = Depends(get_storage_service),
):
    if payload.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValidationError(
            f"Unsupported content type. Allowed: {', '.join(ALLOWED_CONTENT_TYPES)}"
        )

    try:
        object_key = storage.build_object_key(payload.folder, payload.filename)
    except ValueError:
        raise ValidationError(
            f"Unsupported file extension. Allowed: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}"
        )

    result = storage.create_presigned_upload(object_key, payload.content_type)
    return ApiResponse(data=PresignUploadResponse(**result), message="Upload URL created")
