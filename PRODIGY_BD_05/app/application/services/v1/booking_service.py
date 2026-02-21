import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.domain.models.booking import Booking
from app.infrastructure.repositories.booking_repository import BookingRepository
from app.infrastructure.repositories.room_repository import RoomRepository
from app.api.v1.schemas.booking_schema import BookingCreate


class BookingService:
    def __init__(self, booking_repo: BookingRepository, room_repo: RoomRepository):
        self.booking_repo = booking_repo
        self.room_repo = room_repo

    def create(self, db: Session, user_id: str, data: BookingCreate):
        room = self.room_repo.get_by_id(db, data.room_id)

        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        if not room.is_available:
            raise HTTPException(status_code=400, detail="Room unavailable")

        if data.check_in_date >= data.check_out_date:
            raise HTTPException(status_code=400, detail="Invalid dates")

        conflict = self.booking_repo.has_conflict(
            db,
            data.room_id,
            data.check_in_date,
            data.check_out_date,
        )

        if conflict:
            raise HTTPException(status_code=400, detail="Booking conflict, ")

        booking = Booking(
            user_id=uuid.UUID(user_id),
            room_id=data.room_id,
            check_in_date=data.check_in_date,
            check_out_date=data.check_out_date,
            status="confirmed",
        )

        return self.booking_repo.create(db, booking)

    def cancel(self, db: Session, booking_id: str, user_id: str):
        booking = db.query(Booking).filter(Booking.id == uuid.UUID(booking_id)).first()

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if str(booking.user_id) != user_id:
            raise HTTPException(status_code=403, detail="Not your booking")

        booking.status = "cancelled"
        return self.booking_repo.update(db, booking)
