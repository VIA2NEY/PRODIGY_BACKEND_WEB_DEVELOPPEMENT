from fastapi import Depends
from pytest import Session

from app.application.services.v1.auth_service import AuthService
from app.application.services.v1.booking_service import BookingService
from app.application.services.v1.cache_service import CacheService
from app.application.services.v1.hotel_service import HotelService
from app.application.services.v1.room_service import RoomService
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.booking_repository import BookingRepository
from app.infrastructure.repositories.hotel_repository import HotelRepository
from app.infrastructure.repositories.room_repository import RoomRepository
from app.infrastructure.repositories.user_repository import UserRepository



# -----------------------------
# Cache
# -----------------------------

def get_cache_service() -> CacheService:
    return CacheService()


# -----------------------------
# Repositories
# -----------------------------

def get_user_repository(
    db: Session = Depends(get_db)
) -> UserRepository:
    return UserRepository(db)


def get_booking_repository(
    db: Session = Depends(get_db)
) -> BookingRepository:
    return BookingRepository(db)


def get_room_repository(
    db: Session = Depends(get_db)
) -> RoomRepository:
    return RoomRepository(db)


def get_hotel_repository(
    db: Session = Depends(get_db)
) -> HotelRepository:
    return HotelRepository(db)


# -----------------------------
# Services
# -----------------------------

def get_auth_service_v1(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo)


def get_booking_service_v1(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    room_repo: RoomRepository = Depends(get_room_repository),
    cache_service: CacheService = Depends(get_cache_service),
) -> BookingService:
    return BookingService(
        booking_repo,
        room_repo,
        cache_service
    )


def get_hotel_service_v1(
    hotel_repo: HotelRepository = Depends(get_hotel_repository),
    cache_service: CacheService = Depends(get_cache_service),
) -> HotelService:
    return HotelService(hotel_repo, cache_service)


def get_room_service_v1(
    room_repo: RoomRepository = Depends(get_room_repository),
    hotel_repo: HotelRepository = Depends(get_hotel_repository),
    cache_service: CacheService = Depends(get_cache_service),
) -> RoomService:
    return RoomService(
        room_repo,
        hotel_repo,
        cache_service
    )