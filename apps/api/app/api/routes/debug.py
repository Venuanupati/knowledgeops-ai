from fastapi import APIRouter, HTTPException

from app.core.config import settings

router = APIRouter()


@router.get("/debug-error")
def debug_error():
    if settings.APP_ENV != "local":
        raise HTTPException(status_code=404, detail="Not found.")

    raise RuntimeError("Intentional debug error")
