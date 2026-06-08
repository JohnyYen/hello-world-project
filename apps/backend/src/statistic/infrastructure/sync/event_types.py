from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class FeedbackDeliveredEvent(BaseModel):
    event_type: str = "feedback_delivered"
    feedback_id: UUID
    student_id: UUID
    professor_id: UUID
    course_id: UUID
    feedback_type: str
    rating: Optional[int] = None
    comments: str
    display_in_game: bool
    created_at: datetime
