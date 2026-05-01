import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(title=settings.APP_NAME)

allowed_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid4())
    request.state.request_id = request_id

    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time
    response.headers["X-Request-ID"] = request_id

    logger.info(
        "request_id=%s %s %s - %s - %.3f sec",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")

    logger.exception(
        "Unhandled error occurred. request_id=%s path=%s",
        request_id,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred.",
            "request_id": request_id,
        },
    )


@app.get("/", tags=["Root"])
def root():
    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "message": "KnowledgeOps AI API is running.",
        "docs_url": "/docs",
        "health_url": f"{settings.API_V1_PREFIX}/health",
    }


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
