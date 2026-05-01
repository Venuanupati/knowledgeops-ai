from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.document_query import get_document_by_id
from app.services.document_reindex import reindex_document

router = APIRouter()


@router.post("/documents/{document_id}/reindex")
def reindex_existing_document(document_id: int):
    db: Session = SessionLocal()
    try:
        document = get_document_by_id(db, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found.")

        chunks_created = reindex_document(db, document)
    finally:
        db.close()

    return {
        "message": f"Document {document_id} reindexed successfully.",
        "chunks_created": chunks_created,
    }
