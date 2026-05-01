from pydantic import BaseModel


class DocumentItem(BaseModel):
    id: int
    filename: str
    saved_path: str
    content_type: str | None
    status: str
    chunk_count: int
    created_at: str


class DocumentListResponse(BaseModel):
    items: list[DocumentItem]
    total: int
    limit: int
    offset: int
