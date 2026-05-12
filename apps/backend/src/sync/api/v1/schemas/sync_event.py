from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, Union
from uuid import UUID


class SyncEventBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sync_session_id: Union[UUID, str, int] = Field(..., description="ID of the sync session")
    event_type: str = Field(..., description="Type of the event")
    payload: Optional[dict] = Field(None, description="Event payload data")


class SyncEventCreate(SyncEventBase):
    pass


class SyncEventUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: Optional[dict] = Field(None, description="Event payload data")


class SyncEventSchema(SyncEventBase):
    model_config = ConfigDict(from_attributes=True)

    id: Union[str, UUID] = Field(..., description="Event ID")
    timestamp: datetime = Field(..., description="Event timestamp")
    status: Optional[str] = Field(None, description="Event status")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    @field_validator("sync_session_id", mode="before")
    @classmethod
    def convert_sync_session_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v
