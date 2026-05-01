from pydantic import BaseModel


class ChatFeedbackItem(BaseModel):
    id: int
    chat_id: int
    rating: str
    comment: str | None = None
    created_at: str


class ChatFeedbackListResponse(BaseModel):
    items: list[ChatFeedbackItem]
    total: int
    limit: int
    offset: int
