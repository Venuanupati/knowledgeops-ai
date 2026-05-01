from sqlalchemy.orm import Session

from app.db.models import ChatFeedback, ChatLog


def get_chat_log_by_id(db: Session, chat_id: int) -> ChatLog | None:
    return db.query(ChatLog).filter(ChatLog.id == chat_id).first()


def get_chat_feedback_by_id(db: Session, feedback_id: int) -> ChatFeedback | None:
    return db.query(ChatFeedback).filter(ChatFeedback.id == feedback_id).first()


def create_chat_feedback(
    db: Session,
    chat_id: int,
    rating: str,
    comment: str | None = None,
) -> ChatFeedback:
    feedback = ChatFeedback(
        chat_id=chat_id,
        rating=rating,
        comment=comment,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


def get_chat_feedback_items(
    db: Session,
    chat_id: int | None = None,
    rating: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[ChatFeedback]:
    query = db.query(ChatFeedback)

    if chat_id is not None:
        query = query.filter(ChatFeedback.chat_id == chat_id)

    if rating is not None:
        query = query.filter(ChatFeedback.rating == rating)

    return query.order_by(ChatFeedback.id.desc()).offset(offset).limit(limit).all()


def get_total_feedback_count(db: Session) -> int:
    return db.query(ChatFeedback).count()


def get_total_feedback_count_filtered(
    db: Session,
    chat_id: int | None = None,
    rating: str | None = None,
) -> int:
    query = db.query(ChatFeedback)

    if chat_id is not None:
        query = query.filter(ChatFeedback.chat_id == chat_id)

    if rating is not None:
        query = query.filter(ChatFeedback.rating == rating)

    return query.count()


def get_feedback_rating_count(db: Session, rating: str) -> int:
    return db.query(ChatFeedback).filter(ChatFeedback.rating == rating).count()
