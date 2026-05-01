from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk


def get_documents(
    db: Session,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Document]:
    query = db.query(Document)

    if status is not None:
        query = query.filter(Document.status == status)

    return query.order_by(Document.id.desc()).offset(offset).limit(limit).all()


def get_document_chunks(
    db: Session,
    document_id: int,
    limit: int = 20,
    offset: int = 0,
) -> list[DocumentChunk]:
    return (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_document_by_id(db: Session, document_id: int) -> Document | None:
    return db.query(Document).filter(Document.id == document_id).first()


def get_document_chunk_count(db: Session, document_id: int) -> int:
    return db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).count()


def get_document_status_count(db: Session, status: str) -> int:
    return db.query(Document).filter(Document.status == status).count()


def get_total_document_count(db: Session) -> int:
    return db.query(Document).count()


def get_total_document_count_filtered(db: Session, status: str | None = None) -> int:
    query = db.query(Document)

    if status is not None:
        query = query.filter(Document.status == status)

    return query.count()


def delete_document_chunks(db: Session, document_id: int) -> None:
    db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
    db.commit()
