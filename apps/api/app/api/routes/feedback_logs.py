from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.feedback_log import ChatFeedbackItem, ChatFeedbackListResponse
from app.services.datetime_utils import to_iso_string
from app.services.feedback_store import get_chat_feedback_items, get_total_feedback_count_filtered
from app.services.pagination import validate_pagination

router = APIRouter()

ALLOWED_RATING_VALUES = {"up", "down"}


@router.get("/chat-feedback", response_model=ChatFeedbackListResponse)
def read_chat_feedback(
    chat_id: int | None = Query(default=None),
    rating: str | None = Query(default=None),
    limit: int = Query(default=20),
    offset: int = Query(default=0),
):
    validate_pagination(limit, offset)

    if rating is not None and rating not in ALLOWED_RATING_VALUES:
        raise HTTPException(
            status_code=400,
            detail="rating must be one of: up, down.",
        )

    db: Session = SessionLocal()
    try:
        feedback_items = get_chat_feedback_items(
            db,
            chat_id=chat_id,
            rating=rating,
            limit=limit,
            offset=offset,
        )
        total = get_total_feedback_count_filtered(
            db,
            chat_id=chat_id,
            rating=rating,
        )
    finally:
        db.close()

    items = [
        ChatFeedbackItem(
            id=item.id,
            chat_id=item.chat_id,
            rating=item.rating,
            comment=item.comment,
            created_at=to_iso_string(item.created_at),
        )
        for item in feedback_items
    ]

    return ChatFeedbackListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )
