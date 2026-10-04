from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db, require_roles
from app.core.responses import ApiResponse, PaginatedData
from app.models.user import UserRole
from app.schemas.report import ReportCreate, ReportPublic, ReportResolveRequest
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


def get_report_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> ReportService:
    return ReportService(db)


@router.post("", response_model=ApiResponse[ReportPublic], status_code=201)
async def create_report(
    payload: ReportCreate,
    user: dict = Depends(get_current_user),
    service: ReportService = Depends(get_report_service),
):
    report = await service.create_report(user, payload)
    return ApiResponse(data=ReportPublic.model_validate(report), message="Report submitted")


@router.get("", response_model=ApiResponse[PaginatedData[ReportPublic]])
async def list_reports(
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    _admin: dict = Depends(require_roles(UserRole.ADMIN)),
    service: ReportService = Depends(get_report_service),
):
    items, total = await service.list_reports(status, page=page, page_size=page_size)
    return ApiResponse(
        data=PaginatedData(
            items=[ReportPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/{report_id}/resolve", response_model=ApiResponse[ReportPublic])
async def resolve_report(
    report_id: str,
    payload: ReportResolveRequest,
    _admin: dict = Depends(require_roles(UserRole.ADMIN)),
    service: ReportService = Depends(get_report_service),
):
    report = await service.resolve_report(report_id, payload.status.value)
    return ApiResponse(data=ReportPublic.model_validate(report), message="Report updated")
