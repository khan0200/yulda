from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_db
from app.core.responses import ApiResponse
from app.schemas.community import PostPublic
from app.schemas.marketplace import ListingPublic
from app.schemas.search import SearchResults
from app.services.search_service import SearchService

router = APIRouter(tags=["search"])


def get_search_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> SearchService:
    return SearchService(db)


@router.get("/search", response_model=ApiResponse[SearchResults])
async def search(
    q: str = Query(min_length=1, max_length=200),
    service: SearchService = Depends(get_search_service),
):
    results = await service.search(q)
    return ApiResponse(
        data=SearchResults(
            marketplace=[ListingPublic.model_validate(item) for item in results["marketplace"]],
            community=[PostPublic.model_validate(item) for item in results["community"]],
        )
    )
