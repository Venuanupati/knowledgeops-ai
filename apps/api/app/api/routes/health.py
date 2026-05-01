from fastapi import APIRouter

from app.services.health_service import check_postgres, check_qdrant

router = APIRouter()


@router.get("/health")
def health_check():
    postgres_ok = check_postgres()
    qdrant_ok = check_qdrant()

    overall_status = "ok" if postgres_ok and qdrant_ok else "degraded"

    return {
        "status": overall_status,
        "postgres": "ok" if postgres_ok else "down",
        "qdrant": "ok" if qdrant_ok else "down",
    }
