from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.document_summary import DocumentSummaryResponse
from app.services.document_query import (
    get_document_status_count,
    get_total_document_count,
)

router = APIRouter()


@router.get("/documents-summary", response_model=DocumentSummaryResponse)
def read_documents_summary():
    db: Session = SessionLocal()
    try:
        total_documents = get_total_document_count(db)
        uploaded_count = get_document_status_count(db, "uploaded")
        chunked_count = get_document_status_count(db, "chunked")
        indexed_count = get_document_status_count(db, "indexed")
    finally:
        db.close()

    return DocumentSummaryResponse(
        total_documents=total_documents,
        uploaded_count=uploaded_count,
        chunked_count=chunked_count,
        indexed_count=indexed_count,
    )
