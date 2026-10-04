from fastapi import APIRouter

from app.api.v1 import (
    admin,
    auth,
    auto,
    blocks,
    cargo,
    community,
    conversations,
    favorites,
    housing,
    jobs,
    marketplace,
    notifications,
    places,
    reports,
    routes,
    search,
    services,
    uploads,
    users,
    ws,
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
api_router.include_router(conversations.router)
api_router.include_router(notifications.router)
api_router.include_router(ws.router)
api_router.include_router(search.router)
api_router.include_router(reports.router)
api_router.include_router(blocks.router)
api_router.include_router(admin.router)
