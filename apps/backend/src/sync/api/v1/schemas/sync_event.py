from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class SyncEventBase(BaseModel):
    sync_session_id: int = Field(..., description="ID of the sync session")
    event_type: str = Field(..., description="Type of the event")
    payload: Optional[dict] = Field(None, description="Event payload data")


class SyncEventCreate(SyncEventBase):
    pass


class SyncEventUpdate(BaseModel):
    payload: Optional[dict] = Field(None, description="Event payload data")


class SyncEventSchema(SyncEventBase):
    id: str | UUID = Field(..., description="Event ID")
    timestamp: datetime = Field(..., description="Event timestamp")
    status: Optional[str] = Field(None, description="Event status")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    class Config:
        from_attributes = True
