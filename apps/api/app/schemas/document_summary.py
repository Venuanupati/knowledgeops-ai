from pydantic import BaseModel


class DocumentSummaryResponse(BaseModel):
    total_documents: int
    uploaded_count: int
    chunked_count: int
    indexed_count: int
