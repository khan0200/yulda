from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse, PaginatedData
from app.models.job import JobCategory, JobEmploymentType, JobPostType
from app.schemas.job import JobPostCreate, JobPostPublic, JobPostUpdate
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_job_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> JobService:
    return JobService(db)


@router.get("/posts", response_model=ApiResponse[PaginatedData[JobPostPublic]])
async def list_posts(
    post_type: JobPostType | None = None,
    category: JobCategory | None = None,
    employment_type: JobEmploymentType | None = None,
    city: str | None = None,
    requires_korean: bool | None = None,
    visa_sponsorship: bool | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    service: JobService = Depends(get_job_service),
):
    items, total = await service.list_posts(
        post_type=post_type.value if post_type else None,
        category=category.value if category else None,
        employment_type=employment_type.value if employment_type else None,
        city=city,
        requires_korean=requires_korean,
        visa_sponsorship=visa_sponsorship,
        page=page,
        page_size=page_size,
    )
    return ApiResponse(
        data=PaginatedData(
            items=[JobPostPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/posts", response_model=ApiResponse[JobPostPublic], status_code=201)
async def create_post(
    payload: JobPostCreate,
    user: dict = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    post = await service.create_post(user, payload)
    return ApiResponse(data=JobPostPublic.model_validate(post), message="Job post created")


@router.get("/posts/mine", response_model=ApiResponse[PaginatedData[JobPostPublic]])
async def list_my_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    user: dict = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    items, total = await service.list_my_posts(user, page=page, page_size=page_size)
    return ApiResponse(
        data=PaginatedData(
            items=[JobPostPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/posts/{job_id}/repost", response_model=ApiResponse[JobPostPublic])
async def repost_post(
    job_id: str,
    user: dict = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    post = await service.repost_post(job_id, user)
    return ApiResponse(data=JobPostPublic.model_validate(post), message="Job post reposted")


@router.get("/posts/{job_id}", response_model=ApiResponse[JobPostPublic])
async def get_post(job_id: str, service: JobService = Depends(get_job_service)):
    post = await service.get_post(job_id)
    return ApiResponse(data=JobPostPublic.model_validate(post))


@router.patch("/posts/{job_id}", response_model=ApiResponse[JobPostPublic])
async def update_post(
    job_id: str,
    payload: JobPostUpdate,
    user: dict = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    post = await service.update_post(job_id, user, payload)
    return ApiResponse(data=JobPostPublic.model_validate(post), message="Job post updated")


@router.delete("/posts/{job_id}", response_model=ApiResponse[None])
async def delete_post(
    job_id: str,
    user: dict = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    await service.delete_post(job_id, user)
    return ApiResponse(data=None, message="Job post deleted")
