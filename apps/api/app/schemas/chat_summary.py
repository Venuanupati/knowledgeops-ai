from pydantic import BaseModel


class ChatSummaryResponse(BaseModel):
    total_chats: int
    high_confidence_count: int
    medium_confidence_count: int
    low_confidence_count: int
