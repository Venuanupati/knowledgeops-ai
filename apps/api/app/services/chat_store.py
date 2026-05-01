import json

from sqlalchemy.orm import Session

from app.db.models import ChatLog


def create_chat_log(
    db: Session,
    question: str,
    answer: str,
    confidence: str,
    sources: list[dict],
) -> ChatLog:
    chat_log = ChatLog(
        question=question,
        answer=answer,
        confidence=confidence,
        sources_json=json.dumps(sources),
    )
    db.add(chat_log)
    db.commit()
    db.refresh(chat_log)
    return chat_log


def get_chat_logs(
    db: Session,
    chat_id: int | None = None,
    confidence: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[ChatLog]:
    query = db.query(ChatLog)

    if chat_id is not None:
        query = query.filter(ChatLog.id == chat_id)

    if confidence is not None:
        query = query.filter(ChatLog.confidence == confidence)

    return query.order_by(ChatLog.id.desc()).offset(offset).limit(limit).all()


def get_total_chat_count(db: Session) -> int:
    return db.query(ChatLog).count()


def get_total_chat_count_filtered(
    db: Session,
    chat_id: int | None = None,
    confidence: str | None = None,
) -> int:
    query = db.query(ChatLog)

    if chat_id is not None:
        query = query.filter(ChatLog.id == chat_id)

    if confidence is not None:
        query = query.filter(ChatLog.confidence == confidence)

    return query.count()


def get_chat_confidence_count(db: Session, confidence: str) -> int:
    return db.query(ChatLog).filter(ChatLog.confidence == confidence).count()


def get_chat_log_by_id(db: Session, chat_id: int) -> ChatLog | None:
    return db.query(ChatLog).filter(ChatLog.id == chat_id).first()
