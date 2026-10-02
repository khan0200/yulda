import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import close_mongo_connection, connect_to_mongo
from app.core.exceptions import AppError
from app.core.rate_limit import limiter
from app.core.redis import close_redis, connect_to_redis
from app.core.responses import ApiError
from app.middleware.security_headers import SecurityHeadersMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("yulda")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENV != "test":
        await connect_to_mongo()
        await connect_to_redis()
    logger.info("%s backend started", settings.APP_NAME)
    yield
    if settings.ENV != "test":
        await close_mongo_connection()
        await close_redis()


app = FastAPI(
    title=f"{settings.APP_NAME} API",
    version="1.0.0",
    description="Yulda — local marketplace for taxi, delivery, jobs and services.",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiError(error_code=exc.error_code, message=exc.message).model_dump(),
    )


def _sanitize_validation_errors(errors: list[dict]) -> list[dict]:
    sanitized = []
    for error in errors:
        clean = {k: v for k, v in error.items() if k not in ("input", "ctx")}
        if "ctx" in error:
            clean["ctx"] = {k: str(v) for k, v in error["ctx"].items()}
        sanitized.append(clean)
    return sanitized


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=ApiError(
            error_code="VALIDATION_ERROR",
            message="Request validation failed",
            details=jsonable_encoder(_sanitize_validation_errors(exc.errors())),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=ApiError(error_code="INTERNAL_ERROR", message="An unexpected error occurred").model_dump(),
    )


app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
