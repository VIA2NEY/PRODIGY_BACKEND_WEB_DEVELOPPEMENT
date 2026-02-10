from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.application.services.v1.hotel_service import HotelService
from app.infrastructure.repositories.hotel_repository import HotelRepository
from app.api.v1.schemas.hotel_schema import HotelCreate,HotelDetailResponse, HotelListResponse, HotelUpdate
from app.core.security import require_roles, get_current_user

router = APIRouter(prefix="/hotels", tags=["Hotels"])


def get_hotel_service():
    return HotelService(HotelRepository())


@router.post("", response_model=HotelDetailResponse, dependencies=[Depends(require_roles("admin", "owner"))],)
def create_hotel(
    payload: HotelCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_hotel_service()
    hotel = service.create(db, current_user["user_id"], payload)

    return HotelDetailResponse(
        code=201,
        message="Hotel created successfully",
        data=hotel,
    )

@router.put("/{hotel_id}", response_model=HotelDetailResponse, dependencies=[Depends(require_roles("owner"))])
def update_hotel(
    hotel_id: str,
    payload: HotelUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_hotel_service()
    hotel = service.update(db, hotel_id, current_user["user_id"], payload)

    return HotelDetailResponse(
        code=200,
        message="Hotel updated successfully",
        data=hotel,
)

@router.get("", response_model=HotelListResponse)
def list_hotels(service=Depends(get_hotel_service), db: Session = Depends(get_db)):
    service = get_hotel_service()
    hotel = service.list_all(db)
    return HotelListResponse(
        code=200, 
        message="Success", 
        data=hotel
    )