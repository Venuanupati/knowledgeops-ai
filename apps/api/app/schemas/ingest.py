from pydantic import BaseModel


class IngestResponse(BaseModel):
    document_id: int
    filename: str
    saved_path: str
    extracted_text_length: int
    chunks_created: int
    message: str
