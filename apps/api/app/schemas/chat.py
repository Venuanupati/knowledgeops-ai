from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    document_id: int | None = None
    top_k: int | None = None
    include_sources: bool = True


class ChatSource(BaseModel):
    document_id: int
    chunk_id: int
    filename: str
    chunk_index: int
    score: float | None = None
    snippet: str


class ChatResponse(BaseModel):
    chat_id: int
    answer: str
    confidence: str
    sources: list[ChatSource]
