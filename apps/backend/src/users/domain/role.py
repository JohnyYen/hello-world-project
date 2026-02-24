from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Role(Base):
    __tablename__ = "roles"

    role_name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    users = relationship("User", back_populates="role")
