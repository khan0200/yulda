from typing import Literal

from pydantic import BaseModel, Field

UploadFolder = Literal["marketplace", "housing", "auto", "community"]


class PresignUploadRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(min_length=1, max_length=100)
    folder: UploadFolder


class PresignUploadResponse(BaseModel):
    upload_url: str
    public_url: str
