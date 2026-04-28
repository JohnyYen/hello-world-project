from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class SyncSessionBase(BaseModel):
    instance_id: int = Field(..., description="ID of the game instance")
    is_active: bool = Field(True, description="Whether the session is active")


class SyncSessionCreate(SyncSessionBase):
    pass


class SyncSessionUpdate(BaseModel):
    is_active: Optional[bool] = Field(None, description="Whether the session is active")


class SyncSessionSchema(SyncSessionBase):
    id: str | UUID = Field(..., description="Session ID")
    start_time: datetime = Field(..., description="Session start timestamp")
    end_time: Optional[datetime] = Field(None, description="Session end timestamp")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    class Config:
        from_attributes = True
