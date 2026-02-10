from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user, require_roles
from app.infrastructure.repositories.room_repository import RoomRepository
from app.infrastructure.database.session import get_db
from app.api.v1.schemas.room_schema import RoomCreate, RoomDetailResponse, RoomListResponse, RoomUpdate
from app.application.services.v1.room_service import RoomService
from app.infrastructure.repositories.hotel_repository import HotelRepository
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

router = APIRouter(prefix="/rooms", tags=["Rooms"])

def get_room_service():
    return RoomService(RoomRepository(), HotelRepository())


@router.post("/hotel/{hotel_id}",response_model=RoomDetailResponse, dependencies=[Depends(require_roles("owner"))])
def create_room(
    hotel_id: str,
    payload: RoomCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = get_room_service()
    room = service.create(db, hotel_id, current_user["user_id"], payload)

    return RoomDetailResponse(
        code=201,
        message="Room created successfully",
        data=room,
    )

@router.get("/hotel/{hotel_id}", response_model=RoomListResponse)
def list_rooms_by_hotel(hotel_id: str, db: Session = Depends(get_db)):
    service = get_room_service()
    rooms = service.list_by_hotel(db, hotel_id)

    return RoomListResponse(
        code=200,
        message="Success",
        data=rooms
    )

@router.get("/{room_id}/", response_model=RoomDetailResponse)
def get_room(room_id: str, db: Session = Depends(get_db)):
    service = get_room_service()
    room = service.room_repo.get_by_id(db, uuid.UUID(room_id))

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return RoomDetailResponse(
        code=200,
        message="Success",
        data=room
    )


@router.get("/available", response_model=RoomListResponse)
def list_available_rooms(db: Session = Depends(get_db)):

    service = get_room_service()
    rooms = service.list_available(db)

    return RoomListResponse(
        code=200,
        message="Success",
        data=rooms,
    )
@router.put("/{room_id}", response_model=RoomDetailResponse, dependencies=[Depends(require_roles("owner"))])
def update_room(
    room_id: str,
    payload: RoomUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_room_service()
    room = service.update(db, room_id, current_user["user_id"], payload)

    return RoomDetailResponse(
        code=200,
        message="Room updated successfully",
        data=room,
    )

@router.patch("/{room_id}/availability", response_model=RoomDetailResponse, dependencies=[Depends(require_roles("owner"))])
def toggle_room_availability(
    room_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_room_service()
    room = service.toggle_availability(db, room_id, current_user["user_id"])

    return RoomDetailResponse(
        code=200,
        message="Availability updated",
        data=room
    )

@router.delete("/{room_id}", dependencies=[Depends(require_roles("owner"))])
def delete_room(
    room_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_room_service()
    service.delete(db, room_id, current_user["user_id"])

    return {
        "code": 200,
        "message": "Room deleted successfully",
        "data": None,
    }


@router.get("/search", response_model=RoomListResponse)
def search_rooms(
    check_in: datetime,
    check_out: datetime,
    db: Session = Depends(get_db),
):
    service = get_room_service()
    rooms = service.list_available_by_date(db, check_in, check_out)

    return RoomListResponse(
        code=200,
        message="Available rooms",
        data=rooms
    )
