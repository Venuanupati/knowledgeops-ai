import json

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.chat_log import ChatLogItem, ChatLogListResponse, ChatLogSource
from app.services.chat_store import get_chat_logs, get_total_chat_count_filtered
from app.services.datetime_utils import to_iso_string
from app.services.pagination import validate_pagination

router = APIRouter()

ALLOWED_CONFIDENCE_VALUES = {"high", "medium", "low"}


@router.get("/chat-logs", response_model=ChatLogListResponse)
def read_chat_logs(
    chat_id: int | None = Query(default=None),
    confidence: str | None = Query(default=None),
    include_full_text: bool = Query(default=True),
    limit: int = Query(default=20),
    offset: int = Query(default=0),
):
    validate_pagination(limit, offset)

    if confidence is not None and confidence not in ALLOWED_CONFIDENCE_VALUES:
        raise HTTPException(
            status_code=400,
            detail="confidence must be one of: high, medium, low.",
        )

    db: Session = SessionLocal()
    try:
        chat_logs = get_chat_logs(
            db,
            chat_id=chat_id,
            confidence=confidence,
            limit=limit,
            offset=offset,
        )
        total = get_total_chat_count_filtered(
            db,
            chat_id=chat_id,
            confidence=confidence,
        )
    finally:
        db.close()

    items = []

    for log in chat_logs:
        parsed_sources = json.loads(log.sources_json) if log.sources_json else []

        items.append(
            ChatLogItem(
                id=log.id,
                question=log.question,
                answer=log.answer,
                confidence=log.confidence,
                sources=[
                    ChatLogSource(
                        document_id=source.get("document_id"),
                        chunk_id=source.get("chunk_id"),
                        filename=source.get("filename"),
                        chunk_index=source.get("chunk_index"),
                        score=source.get("score"),
                        text=source.get("text") if include_full_text else None,
                    )
                    for source in parsed_sources
                ],
                created_at=to_iso_string(log.created_at),
            )
        )

    return ChatLogListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )
