from pydantic import BaseModel


class ChatLogSource(BaseModel):
    document_id: int | None = None
    chunk_id: int | None = None
    filename: str | None = None
    chunk_index: int | None = None
    score: float | None = None
    text: str | None = None


class ChatLogItem(BaseModel):
    id: int
    question: str
    answer: str
    confidence: str
    sources: list[ChatLogSource]
    created_at: str


class ChatLogListResponse(BaseModel):
    items: list[ChatLogItem]
    total: int
    limit: int
    offset: int
