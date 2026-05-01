from pathlib import Path

from sqlalchemy.orm import Session

from app.db.models import Document
from app.services.vector_store import delete_document_vectors


def delete_document_and_related_data(db: Session, document: Document) -> None:
    document_id = document.id
    file_path = document.saved_path

    delete_document_vectors(document_id=document_id)

    db.delete(document)
    db.commit()

    if file_path:
        path = Path(file_path)
        if path.exists():
            path.unlink()
