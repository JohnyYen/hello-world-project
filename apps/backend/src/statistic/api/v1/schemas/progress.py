from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, List


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
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProgressListResponse(BaseModel):
    items: List[ProgressSchema]
    total: int
    skip: int
    limit: int
