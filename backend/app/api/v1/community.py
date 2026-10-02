from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse, PaginatedData
from app.models.community import PostCategory
from app.schemas.community import CommentCreate, CommentPublic, PostCreate, PostPublic, PostUpdate
from app.services.community_service import CommunityService

router = APIRouter(prefix="/community", tags=["community"])


def get_community_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> CommunityService:
    return CommunityService(db)


@router.get("/posts", response_model=ApiResponse[PaginatedData[PostPublic]])
async def list_posts(
    category: PostCategory | None = None,
    city: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    service: CommunityService = Depends(get_community_service),
):
    items, total = await service.list_posts(
        category=category.value if category else None, city=city, page=page, page_size=page_size
    )
    return ApiResponse(
        data=PaginatedData(
            items=[PostPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/posts", response_model=ApiResponse[PostPublic], status_code=201)
async def create_post(
    payload: PostCreate,
    user: dict = Depends(get_current_user),
    service: CommunityService = Depends(get_community_service),
):
    post = await service.create_post(user, payload)
    return ApiResponse(data=PostPublic.model_validate(post), message="Post created")


@router.get("/posts/{post_id}", response_model=ApiResponse[PostPublic])
async def get_post(post_id: str, service: CommunityService = Depends(get_community_service)):
    post = await service.get_post(post_id)
    return ApiResponse(data=PostPublic.model_validate(post))


@router.patch("/posts/{post_id}", response_model=ApiResponse[PostPublic])
async def update_post(
    post_id: str,
    payload: PostUpdate,
    user: dict = Depends(get_current_user),
    service: CommunityService = Depends(get_community_service),
):
    post = await service.update_post(post_id, user, payload)
    return ApiResponse(data=PostPublic.model_validate(post), message="Post updated")


@router.delete("/posts/{post_id}", response_model=ApiResponse[None])
async def delete_post(
    post_id: str,
    user: dict = Depends(get_current_user),
    service: CommunityService = Depends(get_community_service),
):
    await service.delete_post(post_id, user)
    return ApiResponse(data=None, message="Post deleted")


@router.get("/posts/{post_id}/comments", response_model=ApiResponse[PaginatedData[CommentPublic]])
async def list_comments(
    post_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    service: CommunityService = Depends(get_community_service),
):
    items, total = await service.list_comments(post_id, page=page, page_size=page_size)
    return ApiResponse(
        data=PaginatedData(
            items=[CommentPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/posts/{post_id}/comments", response_model=ApiResponse[CommentPublic], status_code=201)
async def add_comment(
    post_id: str,
    payload: CommentCreate,
    user: dict = Depends(get_current_user),
    service: CommunityService = Depends(get_community_service),
):
    comment = await service.add_comment(post_id, user, payload)
    return ApiResponse(data=CommentPublic.model_validate(comment), message="Comment added")
