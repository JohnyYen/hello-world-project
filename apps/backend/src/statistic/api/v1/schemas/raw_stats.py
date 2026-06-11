from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, Any, List
from uuid import UUID


class RawStatsRecord(BaseModel):
    """RawStats record schema for individual raw stats entries."""
    id: str | UUID
    segment_id: int
    actor_id: str
    attempt_count: int = 0
    error_count: int = 0
    hints_used_count: int = 0
    errors_details: Optional[Any] = None
    efficiency_rating: int = 0
    objectives_completed: int = 0
    status: str
    retry_count: int = 0
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    batch_id: Optional[str] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    class Config:
        from_attributes = True


class RawStatsBulkCreate(BaseModel):
    """Bulk create schema for the /sync/bulk-stats endpoint."""
    records: List[RawStatsRecord]

    @field_validator("records")
    @classmethod
    def validate_records(cls, v):
        if not v:
            raise ValueError("records cannot be empty")
        
        for i, record in enumerate(v):
            if not record.id:
                raise ValueError(f"record[{i}].id is required")
            if record.status not in ["pending_sync", "completed", "failed"]:
                raise ValueError(f"record[{i}].status must be 'pending_sync', 'completed', or 'failed'")
        
        return v

    class Config:
        # Allow extra fields to maintain backward compatibility
        extra = "allow"