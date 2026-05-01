from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.chat_feedback import router as chat_feedback_router
from app.api.routes.chat_log_detail import router as chat_log_detail_router
from app.api.routes.chat_logs import router as chat_logs_router
from app.api.routes.chat_summary import router as chat_summary_router
from app.api.routes.debug import router as debug_router
from app.api.routes.document_chunks import router as document_chunks_router
from app.api.routes.document_delete import router as document_delete_router
from app.api.routes.document_detail import router as document_detail_router
from app.api.routes.document_reindex import router as document_reindex_router
from app.api.routes.documents import router as documents_router
from app.api.routes.documents_summary import router as documents_summary_router
from app.api.routes.feedback_detail import router as feedback_detail_router
from app.api.routes.feedback_logs import router as feedback_logs_router
from app.api.routes.feedback_summary import router as feedback_summary_router
from app.api.routes.health import router as health_router
from app.api.routes.info import router as info_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.ping import router as ping_router
from app.api.routes.status import router as status_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])

api_router.include_router(ingest_router, tags=["Documents"])
api_router.include_router(documents_router, tags=["Documents"])
api_router.include_router(documents_summary_router, tags=["Documents"])
api_router.include_router(document_detail_router, tags=["Documents"])
api_router.include_router(document_chunks_router, tags=["Documents"])
api_router.include_router(document_delete_router, tags=["Documents"])
api_router.include_router(document_reindex_router, tags=["Documents"])

api_router.include_router(chat_router, tags=["Chat"])
api_router.include_router(chat_logs_router, tags=["Chat"])
api_router.include_router(chat_log_detail_router, tags=["Chat"])
api_router.include_router(chat_summary_router, tags=["Chat"])

api_router.include_router(chat_feedback_router, tags=["Feedback"])
api_router.include_router(feedback_logs_router, tags=["Feedback"])
api_router.include_router(feedback_detail_router, tags=["Feedback"])
api_router.include_router(feedback_summary_router, tags=["Feedback"])

api_router.include_router(info_router, tags=["Health"])
api_router.include_router(status_router, tags=["Health"])

api_router.include_router(debug_router, tags=["Debug"])

api_router.include_router(ping_router, tags=["Health"])
