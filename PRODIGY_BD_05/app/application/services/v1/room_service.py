import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.models.rooms import Room
from app.infrastructure.repositories.room_repository import RoomRepository
from app.infrastructure.repositories.hotel_repository import HotelRepository
from app.api.v1.schemas.room_schema import RoomCreate, RoomUpdate


class RoomService:
    def __init__(self, room_repo: RoomRepository, hotel_repo: HotelRepository):
        self.room_repo = room_repo
        self.hotel_repo = hotel_repo

    def create(self, db: Session, hotel_id: str, owner_id: str, data: RoomCreate):
        hotel = self.hotel_repo.get_by_id(db, uuid.UUID(hotel_id))

        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        if str(hotel.owner_id) != owner_id:
            raise HTTPException(status_code=403, detail="Not your hotel")

        room = Room(
            hotel_id=uuid.UUID(hotel_id),
            title=data.title,
            description=data.description,
            price_per_night=data.price_per_night,
            capacity=data.capacity,
        )

        return self.room_repo.create(db, room)

    def update(self, db: Session, room_id: str, owner_id: str, data: RoomUpdate):
        room = self.room_repo.get_by_id(db, uuid.UUID(room_id))

        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        if str(room.hotel.owner_id) != owner_id:
            raise HTTPException(status_code=403, detail="Not your room")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(room, field, value)

        return self.room_repo.update(db, room)

    def delete(self, db: Session, room_id: str, owner_id: str):
        room = self.room_repo.get_by_id(db, uuid.UUID(room_id))

        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        if str(room.hotel.owner_id) != owner_id:
            raise HTTPException(status_code=403, detail="Not your room")

        self.room_repo.delete(db, room)

    def list_available(self, db: Session):
        return self.room_repo.get_all_available_rooms(db)

    def list_by_hotel(self, db: Session, hotel_id: str):
        return self.room_repo.get_all_rooms_by_hotel_id(db, uuid.UUID(hotel_id))

    def get_by_id(self, db: Session, room_id: str):
        return self.room_repo.get_by_id(db, uuid.UUID(room_id))
    
    def toggle_availability(self, db: Session, room_id: str, owner_id: str):
        room = self.room_repo.get_by_id(db, uuid.UUID(room_id))

        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        if str(room.hotel.owner_id) != owner_id:
            raise HTTPException(status_code=403, detail="Not your room")

        room.is_available = not room.is_available
        return self.room_repo.update(db, room)


    def list_available_by_date(self, db: Session, check_in, check_out):
        if check_in >= check_out:
            raise HTTPException(status_code=400, detail="Invalid date range")

        return self.room_repo.get_available_by_date(db, check_in, check_out)