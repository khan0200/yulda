from __future__ import annotations

from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError, ValidationError
from app.models.report import ReportTargetType
from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportCreate

_TARGET_COLLECTIONS = {
    ReportTargetType.USER.value: "users",
    ReportTargetType.MARKETPLACE.value: "marketplace_listings",
    ReportTargetType.HOUSING.value: "housing_listings",
    ReportTargetType.AUTO.value: "auto_listings",
    ReportTargetType.JOBS.value: "job_posts",
    ReportTargetType.SERVICES.value: "service_posts",
    ReportTargetType.COMMUNITY.value: "community_posts",
}


class ReportService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db
        self._repo = ReportRepository(db)

    async def create_report(self, user: dict[str, Any], payload: ReportCreate) -> dict[str, Any]:
        if not ObjectId.is_valid(payload.target_id):
            raise NotFoundError("Target not found")
        target_object_id = ObjectId(payload.target_id)

        if payload.target_type == ReportTargetType.USER and target_object_id == user["_id"]:
            raise ValidationError("You cannot report yourself")

        collection = self._db[_TARGET_COLLECTIONS[payload.target_type.value]]
        target = await collection.find_one({"_id": target_object_id})
        if not target:
            raise NotFoundError("Target not found")

        doc = {
            "reporter": {"_id": user["_id"], "name": user["name"]},
            "target_type": payload.target_type.value,
            "target_id": payload.target_id,
            "reason": payload.reason.value,
            "details": payload.details,
        }
        return await self._repo.create(doc)

    async def list_reports(
        self, status: str | None, page: int, page_size: int
    ) -> tuple[list[dict[str, Any]], int]:
        return await self._repo.list(status, page=page, page_size=page_size)

    async def resolve_report(self, report_id: str, status: str) -> dict[str, Any]:
        report = await self._repo.find_by_id(report_id)
        if not report:
            raise NotFoundError("Report not found")
        return await self._repo.update_status(report["_id"], status)
