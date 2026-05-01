from pydantic import BaseModel


class ChatFeedbackSummaryResponse(BaseModel):
    total_feedback: int
    up_count: int
    down_count: int
