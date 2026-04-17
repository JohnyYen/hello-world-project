from sqlalchemy import Column, String
from src.shared.infrastructure.base import Base


class MetricType(Base):
    __tablename__ = "metric_types"

    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
