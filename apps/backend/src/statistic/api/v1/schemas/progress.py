from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, Any, List
from uuid import UUID


class ProgressBase(BaseModel):
    student_id: int
    segment_level_id: int
    attempt_count: int = 0
    error_count: int = 0
    hints_used_count: int = 0
    errors_details: Optional[Any] = None
    objectives_completed: int = 0
    efficiency_rating: int = 0


class ProgressCreate(ProgressBase):
    pass


class ProgressUpdate(BaseModel):
    attempt_count: Optional[int] = None
    error_count: Optional[int] = None
    hints_used_count: Optional[int] = None
    errors_details: Optional[Any] = None
    objectives_completed: Optional[int] = None
    efficiency_rating: Optional[int] = None


class ProgressSchema(ProgressBase):
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


class ProgressListResponse(BaseModel):
    items: List[ProgressSchema]
    total: int
    skip: int
    limit: int
