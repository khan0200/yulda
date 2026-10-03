from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.job import JobCategory, JobEmploymentType, JobPayType, JobPostStatus, JobPostType
from app.schemas.common import GeoPoint, OwnerSummary


class JobPostCreate(BaseModel):
    post_type: JobPostType
    category: JobCategory
    employment_type: JobEmploymentType
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=5000)
    pay_type: JobPayType | None = None
    pay_amount: int | None = Field(default=None, ge=0, le=1_000_000_000)
    city: str | None = Field(default=None, max_length=100)
    location: GeoPoint | None = None
    requires_korean: bool = False
    visa_sponsorship: bool = False
    photos: list[str] = Field(default_factory=list, max_length=9)
    contact_value: str = Field(min_length=1, max_length=200)


class JobPostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    pay_type: JobPayType | None = None
    pay_amount: int | None = Field(default=None, ge=0, le=1_000_000_000)
    photos: list[str] | None = Field(default=None, max_length=9)
    status: JobPostStatus | None = None


class JobPostPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    post_type: JobPostType
    category: JobCategory
    employment_type: JobEmploymentType
    title: str
    description: str
    pay_type: JobPayType | None = None
    pay_amount: int | None = None
    city: str | None = None
    location: GeoPoint | None = None
    requires_korean: bool = False
    visa_sponsorship: bool = False
    photos: list[str]
    contact_value: str
    status: JobPostStatus
    owner: OwnerSummary
    like_count: int = 0
    created_at: datetime
    updated_at: datetime
