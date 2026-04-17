from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class MetricTypeBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class MetricTypeCreate(MetricTypeBase):
    pass


class MetricTypeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class MetricTypeSchema(MetricTypeBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
