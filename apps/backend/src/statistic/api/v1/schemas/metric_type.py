from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
