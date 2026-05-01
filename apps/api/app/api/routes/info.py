from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/info")
def api_info():
    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "api_version": "v1",
        "docs_url": "/docs",
        "health_url": f"{settings.API_V1_PREFIX}/health",
    }
