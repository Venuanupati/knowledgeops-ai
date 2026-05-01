from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.services.chunker import chunk_text
from app.services.document_parser import extract_text_from_file
from app.services.document_query import delete_document_chunks
from app.services.embedding_service import generate_embedding
from app.services.vector_store import delete_document_vectors, upsert_chunk_vector


def reindex_document(db: Session, document: Document) -> int:
    extracted_text = extract_text_from_file(document.saved_path)
    chunks = chunk_text(extracted_text)

    delete_document_vectors(document_id=document.id)
    delete_document_chunks(db=db, document_id=document.id)

    new_chunk_records = []

    for idx, chunk_text_value in enumerate(chunks):
        chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=idx,
            text=chunk_text_value,
        )
        db.add(chunk)
        db.flush()
        new_chunk_records.append(chunk)

    db.commit()

    for chunk_record in new_chunk_records:
        embedding = generate_embedding(chunk_record.text)

        upsert_chunk_vector(
            chunk_id=chunk_record.id,
            embedding=embedding,
            document_id=document.id,
            filename=document.filename,
            chunk_index=chunk_record.chunk_index,
            text=chunk_record.text,
        )

    return len(new_chunk_records)
