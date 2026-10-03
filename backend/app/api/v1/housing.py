from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse, PaginatedData
from app.models.housing import HousingAmenity, HousingType
from app.schemas.housing import HousingCreate, HousingPublic, HousingUpdate
from app.services.housing_service import HousingService

router = APIRouter(prefix="/housing", tags=["housing"])


def get_housing_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> HousingService:
    return HousingService(db)


@router.get("/listings", response_model=ApiResponse[PaginatedData[HousingPublic]])
async def list_listings(
    housing_type: HousingType | None = None,
    city: str | None = None,
    min_deposit: int | None = Query(default=None, ge=0),
    max_deposit: int | None = Query(default=None, ge=0),
    min_rent: int | None = Query(default=None, ge=0),
    max_rent: int | None = Query(default=None, ge=0),
    amenities: list[HousingAmenity] | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    service: HousingService = Depends(get_housing_service),
):
    items, total = await service.list_listings(
        housing_type=housing_type.value if housing_type else None,
        city=city,
        min_deposit=min_deposit,
        max_deposit=max_deposit,
        min_rent=min_rent,
        max_rent=max_rent,
        amenities=[a.value for a in amenities] if amenities else None,
        page=page,
        page_size=page_size,
    )
    return ApiResponse(
        data=PaginatedData(
            items=[HousingPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/listings", response_model=ApiResponse[HousingPublic], status_code=201)
async def create_listing(
    payload: HousingCreate,
    user: dict = Depends(get_current_user),
    service: HousingService = Depends(get_housing_service),
):
    listing = await service.create_listing(user, payload)
    return ApiResponse(data=HousingPublic.model_validate(listing), message="Listing created")


@router.get("/listings/{listing_id}", response_model=ApiResponse[HousingPublic])
async def get_listing(listing_id: str, service: HousingService = Depends(get_housing_service)):
    listing = await service.get_listing(listing_id)
    return ApiResponse(data=HousingPublic.model_validate(listing))


@router.patch("/listings/{listing_id}", response_model=ApiResponse[HousingPublic])
async def update_listing(
    listing_id: str,
    payload: HousingUpdate,
    user: dict = Depends(get_current_user),
    service: HousingService = Depends(get_housing_service),
):
    listing = await service.update_listing(listing_id, user, payload)
    return ApiResponse(data=HousingPublic.model_validate(listing), message="Listing updated")


@router.delete("/listings/{listing_id}", response_model=ApiResponse[None])
async def delete_listing(
    listing_id: str,
    user: dict = Depends(get_current_user),
    service: HousingService = Depends(get_housing_service),
):
    await service.delete_listing(listing_id, user)
    return ApiResponse(data=None, message="Listing deleted")
