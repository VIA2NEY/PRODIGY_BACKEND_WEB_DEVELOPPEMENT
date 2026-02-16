import uuid

from fastapi import HTTPException
from app.api.v1.schemas.hotel_schema import HotelCreate, HotelUpdate
from app.infrastructure.repositories.hotel_repository import HotelRepository
from app.domain.models.hotels import Hotel
from sqlalchemy.orm import Session
from app.application.services.v1.cache_service import CacheService

class HotelService:
    def __init__(self, repo: HotelRepository):
        self.repo = repo
        self.cache = CacheService()

    def create(self, db: Session, owner_id, data: HotelCreate):
        hotel = Hotel(
            name=data.name,
            description=data.description,
            address=data.address,
            owner_id=uuid.UUID(owner_id)
        )

        # Invalidation
        self.cache.invalidate_pattern("hotels:*")

        return self.repo.create(db, hotel)

    def update(self, db: Session, hotel_id: str, owner_id: str, data: HotelUpdate):
        hotel = self.repo.get_by_id(db, uuid.UUID(hotel_id))

        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        if str(hotel.owner_id) != owner_id:
            raise HTTPException(status_code=403, detail="Not your hotel")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(hotel, field, value)

        # Invalidation
        self.cache.invalidate_pattern("hotels:*")

        return self.repo.update(db, hotel)

    def list_all(self, db: Session):
        cache_key = "hotels:all"

        cached = self.cache.get(cache_key)
        if cached:
            return cached

        hotels = self.repo.get_all(db)

        self.cache.set(cache_key, hotels)
        return hotels
    
    def list_by_owner(self, db: Session, owner_id):
        return self.repo.get_by_owner(db, owner_id)

    def get_by_id(self, db: Session, hotel_id):
        return self.repo.get_by_id(db, hotel_id)