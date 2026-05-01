from pydantic import BaseModel


class ChatFeedbackRequest(BaseModel):
    chat_id: int
    rating: str
    comment: str | None = None


class ChatFeedbackResponse(BaseModel):
    feedback_id: int
    chat_id: int
    rating: str
    comment: str | None = None
    message: str
