import logging
import time

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.chat import ChatRequest, ChatResponse, ChatSource
from app.services.chat_service import answer_question
from app.services.chat_store import create_chat_log

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    start_time = time.perf_counter()

    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if len(question) < settings.MIN_QUESTION_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Question is too short. Minimum length is {settings.MIN_QUESTION_LENGTH} characters.",
        )

    if len(question) > settings.MAX_QUESTION_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Question is too long. Maximum length is {settings.MAX_QUESTION_LENGTH} characters.",
        )

    if request.top_k is not None:
        if request.top_k < settings.MIN_TOP_K or request.top_k > settings.MAX_TOP_K:
            raise HTTPException(
                status_code=400,
                detail=(f"top_k must be between {settings.MIN_TOP_K} and {settings.MAX_TOP_K}."),
            )

    logger.info("Processing chat request")

    answer, retrieved_chunks, confidence = answer_question(
        question=question,
        document_id=request.document_id,
        top_k=request.top_k,
    )

    db: Session = SessionLocal()
    try:
        chat_log = create_chat_log(
            db=db,
            question=question,
            answer=answer,
            confidence=confidence,
            sources=retrieved_chunks,
        )
    finally:
        db.close()

    logger.info("Saved chat log with id=%s", chat_log.id)

    sources = []
    if request.include_sources:
        sources = [
            ChatSource(
                document_id=chunk["document_id"],
                chunk_id=chunk["chunk_id"],
                filename=chunk["filename"],
                chunk_index=chunk["chunk_index"],
                score=chunk.get("score"),
                snippet=chunk["text"][:300],
            )
            for chunk in retrieved_chunks
        ]

    duration_seconds = time.perf_counter() - start_time
    logger.info(
        "Chat completed in %.3f seconds for chat_id=%s with confidence=%s",
        duration_seconds,
        chat_log.id,
        confidence,
    )

    return ChatResponse(
        chat_id=chat_log.id,
        answer=answer,
        confidence=confidence,
        sources=sources,
    )
