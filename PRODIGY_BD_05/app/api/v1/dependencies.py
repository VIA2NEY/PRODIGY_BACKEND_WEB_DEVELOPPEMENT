from app.application.services.v1.auth_service import AuthService
from app.application.services.v1.booking_service import BookingService
from app.application.services.v1.cache_service import CacheService
from app.application.services.v1.hotel_service import HotelService
from app.application.services.v1.room_service import RoomService
from app.infrastructure.repositories.booking_repository import BookingRepository
from app.infrastructure.repositories.hotel_repository import HotelRepository
from app.infrastructure.repositories.room_repository import RoomRepository
from app.infrastructure.repositories.user_repository import UserRepository


def get_auth_service_v1():
    return AuthService(UserRepository())


def get_booking_service_v1():
    return BookingService(BookingRepository(), RoomRepository(), CacheService())


def get_hotel_service_v1():
    return HotelService(HotelRepository(), CacheService())


def get_room_service_v1():
    return RoomService(RoomRepository(), HotelRepository(), CacheService())
