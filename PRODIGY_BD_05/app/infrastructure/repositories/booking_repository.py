import uuid

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.domain.models.booking import Booking

class BookingRepository:
    def __init__(self, db : Session):
        self.db = db

    def get_booking_by_id(self, booking_id: str):
        return self.db.query(Booking).filter(Booking.id == uuid.UUID(booking_id)).first()

    def has_conflict(self, room_id, check_in, check_out):
        return self.db.query(Booking).filter(
            Booking.room_id == room_id,
            or_(
                and_(
                    Booking.check_in_date <= check_in,
                    Booking.check_out_date > check_in,
                    Booking.status == "confirmed"
                ),
                and_(
                    Booking.check_in_date < check_out,
                    Booking.check_out_date >= check_out,
                    Booking.status == "confirmed"
                )
            )
        ).first()

    def create(self, booking: Booking):
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update(self, booking: Booking):
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking