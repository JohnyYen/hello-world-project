from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class FeedbackBase(BaseModel):
    student_id: int
    comments: str
    rating: Optional[int] = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    comments: Optional[str] = None
    rating: Optional[int] = None


class FeedbackSchema(FeedbackBase):
    id: str | UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    class Config:
        from_attributes = True
