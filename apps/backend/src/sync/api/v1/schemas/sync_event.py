from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SyncEventBase(BaseModel):
    sync_session_id: int
    event_type: str
    payload: Optional[dict] = None


class SyncEventCreate(SyncEventBase):
    pass


class SyncEventUpdate(BaseModel):
    payload: Optional[dict] = None


class SyncEventSchema(SyncEventBase):
    id: int
    timestamp: datetime
    status: Optional[str] = None

    class Config:
        from_attributes = True
