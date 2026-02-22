from fastapi import APIRouter, Depends
from app.application.services.v1.booking_service import BookingService
from app.infrastructure.repositories.booking_repository import BookingRepository
from app.infrastructure.database.session import get_db
from app.api.v1.schemas.booking_schema import BookingCreate, BookingDetailResponse
from app.core.security import get_current_user, require_roles
from app.infrastructure.repositories.room_repository import RoomRepository
from sqlalchemy.orm import Session

router = APIRouter(prefix="/bookings", tags=["Bookings"])

def get_booking_service():
    return BookingService(BookingRepository(), RoomRepository())


@router.post("", response_model=BookingDetailResponse, dependencies=[Depends(require_roles("user", "owner", "admin"))])
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_booking_service()
    booking = service.create(db, current_user["user_id"], payload)

    return BookingDetailResponse(
        code=201,
        message="Booking created",
        data=booking
    )

@router.patch("/{booking_id}/cancel", response_model=BookingDetailResponse, dependencies=[Depends(require_roles("user", "owner", "admin"))])
def cancel_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_booking_service()
    booking = service.cancel(db, booking_id, current_user["user_id"])

    return BookingDetailResponse(
        code=200,
        message="Booking cancelled",
        data=booking
    )

# @router.patch("/{booking_id}/confirm", response_model=BookingDetailResponse, dependencies=[Depends(require_roles("owner"))])
# def confirm_booking(
#     booking_id: str,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     service = get_booking_service()
#     booking = service.confirm(db, booking_id, current_user["user_id"])

#     return BookingDetailResponse(
#         code=200,
#         message="Booking confirmed",
#         data=booking
# )