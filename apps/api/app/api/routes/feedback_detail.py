from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.feedback_log import ChatFeedbackItem
from app.services.datetime_utils import to_iso_string
from app.services.feedback_store import get_chat_feedback_by_id

router = APIRouter()


@router.get("/chat-feedback/{feedback_id}", response_model=ChatFeedbackItem)
def read_chat_feedback_detail(feedback_id: int):
    db: Session = SessionLocal()
    try:
        feedback = get_chat_feedback_by_id(db, feedback_id)
    finally:
        db.close()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found.")

    return ChatFeedbackItem(
        id=feedback.id,
        chat_id=feedback.chat_id,
        rating=feedback.rating,
        comment=feedback.comment,
        created_at=to_iso_string(feedback.created_at),
    )
