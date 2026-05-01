from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.chat_store import get_total_chat_count
from app.services.document_query import get_total_document_count
from app.services.feedback_store import get_total_feedback_count

router = APIRouter()


@router.get("/status")
def api_status():
    db: Session = SessionLocal()
    try:
        total_documents = get_total_document_count(db)
        total_chats = get_total_chat_count(db)
        total_feedback = get_total_feedback_count(db)
    finally:
        db.close()

    return {
        "status": "ok",
        "total_documents": total_documents,
        "total_chats": total_chats,
        "total_feedback": total_feedback,
    }
