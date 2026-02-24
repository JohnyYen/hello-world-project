from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.shared.infrastructure.base import Base


class Professor(Base):
    __tablename__ = "professors"

    department = Column(String(255), nullable=False)
    contact_phone = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="professor")
