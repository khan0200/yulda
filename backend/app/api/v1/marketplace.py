from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse, PaginatedData
from app.models.marketplace import ListingCategory, ListingCondition
from app.schemas.marketplace import ListingCreate, ListingPublic, ListingUpdate
from app.services.marketplace_service import MarketplaceService

router = APIRouter(prefix="/marketplace", tags=["marketplace"])


def get_marketplace_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> MarketplaceService:
    return MarketplaceService(db)


@router.get("/listings", response_model=ApiResponse[PaginatedData[ListingPublic]])
async def list_listings(
    category: ListingCategory | None = None,
    city: str | None = None,
    condition: ListingCondition | None = None,
    min_price: int | None = Query(default=None, ge=0),
    max_price: int | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    service: MarketplaceService = Depends(get_marketplace_service),
):
    items, total = await service.list_listings(
        category=category.value if category else None,
        city=city,
        condition=condition.value if condition else None,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
    )
    return ApiResponse(
        data=PaginatedData(
            items=[ListingPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/listings", response_model=ApiResponse[ListingPublic], status_code=201)
async def create_listing(
    payload: ListingCreate,
    user: dict = Depends(get_current_user),
    service: MarketplaceService = Depends(get_marketplace_service),
):
    listing = await service.create_listing(user, payload)
    return ApiResponse(data=ListingPublic.model_validate(listing), message="Listing created")


@router.get("/listings/{listing_id}", response_model=ApiResponse[ListingPublic])
async def get_listing(listing_id: str, service: MarketplaceService = Depends(get_marketplace_service)):
    listing = await service.get_listing(listing_id)
    return ApiResponse(data=ListingPublic.model_validate(listing))


@router.patch("/listings/{listing_id}", response_model=ApiResponse[ListingPublic])
async def update_listing(
    listing_id: str,
    payload: ListingUpdate,
    user: dict = Depends(get_current_user),
    service: MarketplaceService = Depends(get_marketplace_service),
):
    listing = await service.update_listing(listing_id, user, payload)
    return ApiResponse(data=ListingPublic.model_validate(listing), message="Listing updated")


@router.delete("/listings/{listing_id}", response_model=ApiResponse[None])
async def delete_listing(
    listing_id: str,
    user: dict = Depends(get_current_user),
    service: MarketplaceService = Depends(get_marketplace_service),
):
    await service.delete_listing(listing_id, user)
    return ApiResponse(data=None, message="Listing deleted")
