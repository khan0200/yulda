from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pyobjectid import PyObjectId
from app.models.report import ReportReason, ReportStatus, ReportTargetType


class ReporterSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    name: str


class ReportCreate(BaseModel):
    target_type: ReportTargetType
    target_id: str = Field(max_length=64)
    reason: ReportReason
    details: str | None = Field(default=None, max_length=1000)


class ReportResolveRequest(BaseModel):
    status: ReportStatus = Field(default=ReportStatus.RESOLVED)


class ReportPublic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(validation_alias="_id", serialization_alias="id")
    reporter: ReporterSummary
    target_type: ReportTargetType
    target_id: str
    reason: ReportReason
    details: str | None = None
    status: ReportStatus
    created_at: datetime
    resolved_at: datetime | None = None
