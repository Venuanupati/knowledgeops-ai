from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.document import DocumentItem, DocumentListResponse
from app.services.datetime_utils import to_iso_string
from app.services.document_query import (
    get_document_chunk_count,
    get_documents,
    get_total_document_count_filtered,
)
from app.services.pagination import validate_pagination

router = APIRouter()

ALLOWED_DOCUMENT_STATUSES = {"uploaded", "chunked", "indexed"}


@router.get("/documents", response_model=DocumentListResponse)
def read_documents(
    status: str | None = Query(default=None),
    limit: int = Query(default=20),
    offset: int = Query(default=0),
):
    validate_pagination(limit, offset)

    if status is not None and status not in ALLOWED_DOCUMENT_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="status must be one of: uploaded, chunked, indexed.",
        )

    db: Session = SessionLocal()
    try:
        documents = get_documents(
            db,
            status=status,
            limit=limit,
            offset=offset,
        )
        total = get_total_document_count_filtered(db, status=status)

        items = [
            DocumentItem(
                id=document.id,
                filename=document.filename,
                saved_path=document.saved_path,
                content_type=document.content_type,
                status=document.status,
                chunk_count=get_document_chunk_count(db, document.id),
                created_at=to_iso_string(document.created_at),
            )
            for document in documents
        ]

        return DocumentListResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
        )
    finally:
        db.close()
