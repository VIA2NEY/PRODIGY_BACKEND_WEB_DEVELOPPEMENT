import uuid

from fastapi import HTTPException
from app.api.v1.schemas.hotel_schema import HotelCreate
from app.infrastructure.repositories.hotel_repository import HotelRepository
from app.domain.models.hotels import Hotel
from sqlalchemy.orm import Session

class HotelService:
    def __init__(self, repo: HotelRepository):
        self.repo = repo

    def create(self, db: Session, owner_id, data: HotelCreate):
        hotel = Hotel(
            name=data.name,
            description=data.description,
            address=data.address,
            owner_id=uuid.UUID(owner_id)
        )
        return self.repo.create(db, hotel)
    
    def update(self, db: Session, hotel_id: str, owner_id: str, data: HotelCreate):
        hotel = self.repo.get_by_id(db, uuid.UUID(hotel_id))

        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        if str(hotel.owner_id) != owner_id:
            raise HTTPException(status_code=403, detail="Not your hotel")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(hotel, field, value)

        return self.repo.update(db, hotel)

    def list_all(self, db: Session):
        return self.repo.get_all(db)

    def list_by_owner(self, db: Session, owner_id):
        return self.repo.get_by_owner(db, owner_id)

    def get_by_id(self, db: Session, hotel_id):
        return self.repo.get_by_id(db, hotel_id)