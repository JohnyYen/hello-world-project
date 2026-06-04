from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.shared.domain.enums import FeedbackType


class FeedbackBase(BaseModel):
    student_id: UUID
    comments: str = Field(..., min_length=1)
    rating: Optional[int] = Field(None, ge=1, le=5)
    feedback_type: FeedbackType = FeedbackType.ADVICE


class FeedbackCreate(FeedbackBase):
    course_id: Optional[UUID] = None
    display_in_game: bool = False


class FeedbackUpdate(BaseModel):
    comments: Optional[str] = None
    rating: Optional[int] = None


class FeedbackSchema(FeedbackBase):
    id: UUID
    professor_id: UUID
    course_id: Optional[UUID] = None
    display_in_game: bool = False
    acknowledged_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class FeedbackListResponse(BaseModel):
    items: list[FeedbackSchema]
    total: int
    skip: int
    limit: int
