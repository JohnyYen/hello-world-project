from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, Union
from uuid import UUID


class SyncSessionBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instance_id: Union[UUID, str, int] = Field(..., description="ID of the game instance")
    is_active: bool = Field(True, description="Whether the session is active")


class SyncSessionCreate(SyncSessionBase):
    pass


class SyncSessionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_active: Optional[bool] = Field(None, description="Whether the session is active")


class SyncSessionSchema(SyncSessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: Union[str, UUID] = Field(..., description="Session ID")
    start_time: datetime = Field(..., description="Session start timestamp")
    end_time: Optional[datetime] = Field(None, description="Session end timestamp")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    @field_validator("instance_id", mode="before")
    @classmethod
    def convert_instance_id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v