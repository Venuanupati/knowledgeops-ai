from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk


def create_document(
    db: Session,
    filename: str,
    saved_path: str,
    content_type: str | None,
    status: str = "uploaded",
) -> Document:
    document = Document(
        filename=filename,
        saved_path=saved_path,
        content_type=content_type,
        status=status,
    )
    db.add(document)
    db.flush()
    db.commit()
    db.refresh(document)
    return document


def create_document_chunks(
    db: Session,
    document_id: int,
    chunks: list[str],
) -> list[DocumentChunk]:
    chunk_records = []

    for idx, chunk_text in enumerate(chunks):
        chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=idx,
            text=chunk_text,
        )
        db.add(chunk)
        db.flush()
        chunk_records.append(chunk)

    db.commit()
    return chunk_records


def update_document_status(
    db: Session,
    document: Document,
    status: str,
) -> Document:
    document.status = status
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
