from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_hotel_service_v1
from app.application.services.v1.hotel_service import HotelService
from app.api.v1.schemas.hotel_schema import HotelCreate,HotelDetailResponse, HotelListResponse, HotelUpdate
from app.core.security import require_roles, get_current_user

router = APIRouter(prefix="/hotels", tags=["Hotels"])



@router.post("", response_model=HotelDetailResponse, dependencies=[Depends(require_roles("admin", "owner"))],)
def create_hotel(
    payload: HotelCreate,
    current_user=Depends(get_current_user),
    service : HotelService = Depends(get_hotel_service_v1),
):
    hotel = service.create(current_user["user_id"], payload)

    return HotelDetailResponse(
        code=201,
        message="Hotel created successfully",
        data=hotel,
    )

@router.put("/{hotel_id}", response_model=HotelDetailResponse, dependencies=[Depends(require_roles("owner"))])
def update_hotel(
    hotel_id: str,
    payload: HotelUpdate,
    current_user=Depends(get_current_user),
    service : HotelService = Depends(get_hotel_service_v1),
):
    hotel = service.update(hotel_id, current_user["user_id"], payload)

    return HotelDetailResponse(
        code=200,
        message="Hotel updated successfully",
        data=hotel,
)

@router.get("", response_model=HotelListResponse)
def list_hotels(service : HotelService = Depends(get_hotel_service_v1)):

    hotel = service.list_all()
    return HotelListResponse(
        code=200, 
        message="Success", 
        data=hotel
    )