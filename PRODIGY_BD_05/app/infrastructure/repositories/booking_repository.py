from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.domain.models.booking import Booking

class BookingRepository:

    def has_conflict(self, db: Session, room_id, check_in, check_out):
        return db.query(Booking).filter(
            Booking.room_id == room_id,
            or_(
                and_(
                    Booking.check_in_date <= check_in,
                    Booking.check_out_date > check_in
                ),
                and_(
                    Booking.check_in_date < check_out,
                    Booking.check_out_date >= check_out
                )
            )
        ).first()

    def create(self, db: Session, booking: Booking):
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    def update(self, db: Session, booking: Booking):
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking