import uuid

from fastapi import HTTPException
from app.api.v1.schemas.hotel_schema import HotelCreate, HotelResponse, HotelUpdate
from app.infrastructure.repositories.hotel_repository import HotelRepository
from app.domain.models.hotels import Hotel
from sqlalchemy.orm import Session
from app.application.services.v1.cache_service import CacheService

class HotelService:
    def __init__(self, repo: HotelRepository, cache: CacheService):
        self.repo = repo
        self.cache = cache

    def create(self, owner_id, data: HotelCreate):
        hotel = Hotel(
            name=data.name,
            description=data.description,
            address=data.address,
            owner_id=uuid.UUID(owner_id)
        )

        # Invalidation
        self.cache.invalidate_pattern("hotels:*")

        return self.repo.create(hotel)

    def update(self, hotel_id: str, owner_id: str, data: HotelUpdate):
        hotel = self.repo.get_by_id(uuid.UUID(hotel_id))

        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        if str(hotel.owner_id) != owner_id:
            raise HTTPException(status_code=403, detail="Not your hotel")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(hotel, field, value)

        # Invalidation
        self.cache.invalidate_pattern("hotels:*")

        return self.repo.update(hotel)

    def list_all(self):
        cache_key = "hotels:all"

        cached = self.cache.get(cache_key)
        if cached:
            return cached

        hotels = self.repo.get_all()

        serialized_cache_response = [
            HotelResponse.model_validate(h).model_dump()
            for h in hotels
        ]

        self.cache.set(cache_key, serialized_cache_response)
        return hotels
    
    def list_by_owner(self, owner_id):
        return self.repo.get_by_owner(owner_id)

    def get_by_id(self, hotel_id):
        return self.repo.get_by_id(hotel_id)