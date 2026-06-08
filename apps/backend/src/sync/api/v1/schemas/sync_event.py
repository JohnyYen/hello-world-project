from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Union
from uuid import UUID


class SyncEventBase(BaseModel):
    sync_session_id: Union[str, UUID] = Field(..., description="ID of the sync session (UUID)")
    event_type: str = Field(..., description="Type of the event")
    payload: Optional[dict] = Field(None, description="Event payload data")

    @field_validator("sync_session_id", mode="before")
    @classmethod
    def convert_session_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class SyncEventCreate(SyncEventBase):
    client_event_id: Optional[UUID] = Field(
        None, description="Client-generated UUID for idempotent event creation"
    )


class SyncEventUpdate(BaseModel):
    payload: Optional[dict] = Field(None, description="Event payload data")


class SyncEventSchema(SyncEventBase):
    id: Union[str, int] = Field(..., description="Event ID")
    timestamp: datetime = Field(..., description="Event timestamp")
    status: Optional[str] = Field(None, description="Event status")

    class Config:
        from_attributes = True

    @field_validator("id", mode="before")
    @classmethod
    def convert_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v
