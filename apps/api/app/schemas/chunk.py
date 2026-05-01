from pydantic import BaseModel


class ChunkItem(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    text: str | None = None
    created_at: str


class ChunkListResponse(BaseModel):
    items: list[ChunkItem]
    total: int
    limit: int
    offset: int
