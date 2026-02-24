from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SyncSessionBase(BaseModel):
    instance_id: int
    is_active: bool = True


class SyncSessionCreate(SyncSessionBase):
    pass


class SyncSessionUpdate(BaseModel):
    is_active: Optional[bool] = None


class SyncSessionSchema(SyncSessionBase):
    id: int
    started_at: datetime
    ended_at: Optional[datetime] = None

    class Config:
        from_attributes = True
