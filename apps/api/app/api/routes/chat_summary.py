from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.chat_summary import ChatSummaryResponse
from app.services.chat_store import get_chat_confidence_count, get_total_chat_count

router = APIRouter()


@router.get("/chat-summary", response_model=ChatSummaryResponse)
def read_chat_summary():
    db: Session = SessionLocal()
    try:
        total_chats = get_total_chat_count(db)
        high_confidence_count = get_chat_confidence_count(db, "high")
        medium_confidence_count = get_chat_confidence_count(db, "medium")
        low_confidence_count = get_chat_confidence_count(db, "low")
    finally:
        db.close()

    return ChatSummaryResponse(
        total_chats=total_chats,
        high_confidence_count=high_confidence_count,
        medium_confidence_count=medium_confidence_count,
        low_confidence_count=low_confidence_count,
    )
