from fastapi import APIRouter

from app.api.v1 import (
    auth,
    auto,
    cargo,
    community,
    favorites,
    housing,
    jobs,
    marketplace,
    places,
    routes,
    services,
    uploads,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(community.router)
api_router.include_router(places.router)
api_router.include_router(marketplace.router)
api_router.include_router(housing.router)
api_router.include_router(auto.router)
api_router.include_router(routes.router)
api_router.include_router(cargo.router)
api_router.include_router(uploads.router)
api_router.include_router(favorites.router)
api_router.include_router(jobs.router)
api_router.include_router(services.router)
