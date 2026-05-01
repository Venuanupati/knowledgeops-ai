from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.chunk import ChunkItem, ChunkListResponse
from app.services.datetime_utils import to_iso_string
from app.services.document_query import get_document_chunk_count, get_document_chunks
from app.services.pagination import validate_pagination

router = APIRouter()


@router.get("/documents/{document_id}/chunks", response_model=ChunkListResponse)
def read_document_chunks(
    document_id: int,
    include_full_text: bool = Query(default=True),
    limit: int = Query(default=20),
    offset: int = Query(default=0),
):
    validate_pagination(limit, offset)

    db: Session = SessionLocal()
    try:
        chunks = get_document_chunks(
            db,
            document_id=document_id,
            limit=limit,
            offset=offset,
        )
        total = get_document_chunk_count(db, document_id)
    finally:
        db.close()

    if total == 0:
        raise HTTPException(status_code=404, detail="No chunks found for this document.")

    items = [
        ChunkItem(
            id=chunk.id,
            document_id=chunk.document_id,
            chunk_index=chunk.chunk_index,
            text=chunk.text if include_full_text else None,
            created_at=to_iso_string(chunk.created_at),
        )
        for chunk in chunks
    ]

    return ChunkListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )
