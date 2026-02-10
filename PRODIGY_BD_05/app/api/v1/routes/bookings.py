from fastapi import APIRouter, Depends
# from app.application.services.v1.booking_service import BookingService
from app.infrastructure.repositories.booking_repository import BookingRepository
from app.infrastructure.database.session import get_db
from app.api.v1.schemas.booking_schema import BookingCreate
from app.core.security import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# def get_service(db=Depends(get_db)):
#     return BookingService(BookingRepository(db))

# @router.post("")
# def book(data: BookingCreate, user=Depends(get_current_user), service=Depends(get_service)):
#     return service.create(user["user_id"], data)
