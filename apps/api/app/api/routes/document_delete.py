from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.document_delete import delete_document_and_related_data
from app.services.document_query import get_document_by_id

router = APIRouter()


@router.delete("/documents/{document_id}")
def delete_document(document_id: int):
    db: Session = SessionLocal()
    try:
        document = get_document_by_id(db, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found.")

        delete_document_and_related_data(db, document)
    finally:
        db.close()

    return {"message": f"Document {document_id} deleted successfully."}
