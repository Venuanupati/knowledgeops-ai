from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.document import DocumentItem
from app.services.datetime_utils import to_iso_string
from app.services.document_query import get_document_by_id, get_document_chunk_count

router = APIRouter()


@router.get("/documents/{document_id}", response_model=DocumentItem)
def read_document(document_id: int):
    db: Session = SessionLocal()
    try:
        document = get_document_by_id(db, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found.")

        chunk_count = get_document_chunk_count(db, document_id)
    finally:
        db.close()

    return DocumentItem(
        id=document.id,
        filename=document.filename,
        saved_path=document.saved_path,
        content_type=document.content_type,
        status=document.status,
        chunk_count=chunk_count,
        created_at=to_iso_string(document.created_at),
    )
