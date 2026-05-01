from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.feedback_summary import ChatFeedbackSummaryResponse
from app.services.feedback_store import get_feedback_rating_count, get_total_feedback_count

router = APIRouter()


@router.get("/chat-feedback-summary", response_model=ChatFeedbackSummaryResponse)
def read_chat_feedback_summary():
    db: Session = SessionLocal()
    try:
        total_feedback = get_total_feedback_count(db)
        up_count = get_feedback_rating_count(db, "up")
        down_count = get_feedback_rating_count(db, "down")
    finally:
        db.close()

    return ChatFeedbackSummaryResponse(
        total_feedback=total_feedback,
        up_count=up_count,
        down_count=down_count,
    )
