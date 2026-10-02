from fastapi import APIRouter

from app.api.v1 import auth, auto, cargo, community, housing, marketplace, places, routes, users

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
