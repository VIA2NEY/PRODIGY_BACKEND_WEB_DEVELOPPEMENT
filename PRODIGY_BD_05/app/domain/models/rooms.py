import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.domain.mixins.timestamp_mixin import TimeStamp
from app.infrastructure.database.base import Base

class Room(Base, TimeStamp):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String)
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)


    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")