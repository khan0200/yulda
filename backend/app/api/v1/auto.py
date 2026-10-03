from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_current_user, get_db
from app.core.responses import ApiResponse, PaginatedData
from app.models.auto import AccidentHistory, AutoListingType, BodyType, FuelType, TransmissionType
from app.schemas.auto import AutoListingCreate, AutoListingPublic, AutoListingUpdate
from app.services.auto_service import AutoService

router = APIRouter(prefix="/auto", tags=["auto"])


def get_auto_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> AutoService:
    return AutoService(db)


@router.get("/listings", response_model=ApiResponse[PaginatedData[AutoListingPublic]])
async def list_listings(
    listing_type: AutoListingType | None = None,
    make: str | None = None,
    fuel_type: FuelType | None = None,
    transmission: TransmissionType | None = None,
    city: str | None = None,
    min_year: int | None = Query(default=None, ge=1980, le=2100),
    max_year: int | None = Query(default=None, ge=1980, le=2100),
    min_price: int | None = Query(default=None, ge=0),
    max_price: int | None = Query(default=None, ge=0),
    min_mileage: int | None = Query(default=None, ge=0),
    max_mileage: int | None = Query(default=None, ge=0),
    body_type: BodyType | None = None,
    color: str | None = None,
    accident_history: AccidentHistory | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    service: AutoService = Depends(get_auto_service),
):
    items, total = await service.list_listings(
        listing_type=listing_type.value if listing_type else None,
        make=make,
        fuel_type=fuel_type.value if fuel_type else None,
        transmission=transmission.value if transmission else None,
        city=city,
        min_year=min_year,
        max_year=max_year,
        min_price=min_price,
        max_price=max_price,
        min_mileage=min_mileage,
        max_mileage=max_mileage,
        body_type=body_type.value if body_type else None,
        color=color,
        accident_history=accident_history.value if accident_history else None,
        page=page,
        page_size=page_size,
    )
    return ApiResponse(
        data=PaginatedData(
            items=[AutoListingPublic.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )
    )


@router.post("/listings", response_model=ApiResponse[AutoListingPublic], status_code=201)
async def create_listing(
    payload: AutoListingCreate,
    user: dict = Depends(get_current_user),
    service: AutoService = Depends(get_auto_service),
):
    listing = await service.create_listing(user, payload)
    return ApiResponse(data=AutoListingPublic.model_validate(listing), message="Listing created")


@router.get("/listings/{listing_id}", response_model=ApiResponse[AutoListingPublic])
async def get_listing(listing_id: str, service: AutoService = Depends(get_auto_service)):
    listing = await service.get_listing(listing_id)
    return ApiResponse(data=AutoListingPublic.model_validate(listing))


@router.patch("/listings/{listing_id}", response_model=ApiResponse[AutoListingPublic])
async def update_listing(
    listing_id: str,
    payload: AutoListingUpdate,
    user: dict = Depends(get_current_user),
    service: AutoService = Depends(get_auto_service),
):
    listing = await service.update_listing(listing_id, user, payload)
    return ApiResponse(data=AutoListingPublic.model_validate(listing), message="Listing updated")


@router.delete("/listings/{listing_id}", response_model=ApiResponse[None])
async def delete_listing(
    listing_id: str,
    user: dict = Depends(get_current_user),
    service: AutoService = Depends(get_auto_service),
):
    await service.delete_listing(listing_id, user)
    return ApiResponse(data=None, message="Listing deleted")
