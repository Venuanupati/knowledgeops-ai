import json

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.chat_log import ChatLogItem, ChatLogSource
from app.services.chat_store import get_chat_log_by_id
from app.services.datetime_utils import to_iso_string

router = APIRouter()


@router.get("/chat-logs/{chat_id}", response_model=ChatLogItem)
def read_chat_log_detail(
    chat_id: int,
    include_full_text: bool = Query(default=True),
):
    db: Session = SessionLocal()
    try:
        chat_log = get_chat_log_by_id(db, chat_id)
    finally:
        db.close()

    if not chat_log:
        raise HTTPException(status_code=404, detail="Chat log not found.")

    parsed_sources = json.loads(chat_log.sources_json) if chat_log.sources_json else []

    return ChatLogItem(
        id=chat_log.id,
        question=chat_log.question,
        answer=chat_log.answer,
        confidence=chat_log.confidence,
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
        created_at=to_iso_string(chat_log.created_at),
    )
