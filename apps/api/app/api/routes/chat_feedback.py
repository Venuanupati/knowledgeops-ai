from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.feedback import ChatFeedbackRequest, ChatFeedbackResponse
from app.services.feedback_store import create_chat_feedback, get_chat_log_by_id

router = APIRouter()


@router.post("/chat-feedback", response_model=ChatFeedbackResponse)
def submit_chat_feedback(request: ChatFeedbackRequest):
    if request.rating not in {"up", "down"}:
        raise HTTPException(status_code=400, detail="Rating must be 'up' or 'down'.")

    db: Session = SessionLocal()
    try:
        chat_log = get_chat_log_by_id(db, request.chat_id)
        if not chat_log:
            raise HTTPException(status_code=404, detail="Chat log not found.")

        feedback = create_chat_feedback(
            db=db,
            chat_id=request.chat_id,
            rating=request.rating,
            comment=request.comment,
        )
    finally:
        db.close()

    return ChatFeedbackResponse(
        feedback_id=feedback.id,
        chat_id=feedback.chat_id,
        rating=feedback.rating,
        comment=feedback.comment,
        message="Feedback submitted successfully.",
    )
