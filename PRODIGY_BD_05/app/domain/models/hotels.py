import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.domain.mixins.timestamp_mixin import TimeStamp
from app.infrastructure.database.base import Base

class Hotel(Base, TimeStamp):
    __tablename__ = "hotels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String, nullable=False)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    
    owner = relationship("User", backref="hotels")
    rooms = relationship("Room", back_populates="hotel", cascade="all, delete")
