from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SyncEventBase(BaseModel):
    sync_session_id: int = Field(..., description="ID of the sync session")
    event_type: str = Field(..., description="Type of the event")
    payload: Optional[dict] = Field(None, description="Event payload data")


class SyncEventCreate(SyncEventBase):
    pass


class SyncEventUpdate(BaseModel):
    payload: Optional[dict] = Field(None, description="Event payload data")


class SyncEventSchema(SyncEventBase):
    id: int = Field(..., description="Event ID")
    timestamp: datetime = Field(..., description="Event timestamp")
    status: Optional[str] = Field(None, description="Event status")

    class Config:
        from_attributes = True
