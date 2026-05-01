import logging
import time

from fastapi import APIRouter, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.ingest import IngestResponse
from app.services.chunker import chunk_text
from app.services.document_parser import extract_text_from_file
from app.services.document_store import (
    create_document,
    create_document_chunks,
    update_document_status,
)
from app.services.embedding_service import generate_embedding
from app.services.file_service import save_uploaded_file, validate_uploaded_file
from app.services.vector_store import upsert_chunk_vector

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ingest", response_model=IngestResponse)
def ingest_file(file: UploadFile = File(...)):
    start_time = time.perf_counter()

    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    try:
        validate_uploaded_file(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logger.info("Received file upload: %s", file.filename)

    saved_filename, saved_path = save_uploaded_file(file)
    logger.info("Saved file to path: %s", saved_path)

    try:
        extracted_text = extract_text_from_file(saved_path)
    except ValueError as exc:
        logger.exception("Unsupported file type for file: %s", saved_path)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logger.info("Extracted text length: %s", len(extracted_text))

    chunks = chunk_text(extracted_text)
    logger.info("Created %s chunks for file: %s", len(chunks), saved_filename)

    db: Session = SessionLocal()
    try:
        document = create_document(
            db=db,
            filename=saved_filename,
            saved_path=saved_path,
            content_type=file.content_type,
            status="uploaded",
        )
        logger.info("Created document_id=%s with status=uploaded", document.id)

        chunk_records = create_document_chunks(
            db=db,
            document_id=document.id,
            chunks=chunks,
        )
        document = update_document_status(db=db, document=document, status="chunked")
        logger.info(
            "Stored %s chunks in Postgres for document_id=%s and updated status=chunked",
            len(chunk_records),
            document.id,
        )

        for chunk_record in chunk_records:
            embedding = generate_embedding(chunk_record.text)

            upsert_chunk_vector(
                chunk_id=chunk_record.id,
                embedding=embedding,
                document_id=document.id,
                filename=document.filename,
                chunk_index=chunk_record.chunk_index,
                text=chunk_record.text,
            )

        document = update_document_status(db=db, document=document, status="indexed")
        logger.info(
            "Indexed %s chunks in Qdrant for document_id=%s and updated status=indexed",
            len(chunk_records),
            document.id,
        )

    finally:
        db.close()

    duration_seconds = time.perf_counter() - start_time
    logger.info("Ingest completed in %.3f seconds for document_id=%s", duration_seconds, document.id)

    return IngestResponse(
        document_id=document.id,
        filename=saved_filename,
        saved_path=saved_path,
        extracted_text_length=len(extracted_text),
        chunks_created=len(chunks),
        message="File uploaded, processed, stored, and indexed successfully.",
    )
