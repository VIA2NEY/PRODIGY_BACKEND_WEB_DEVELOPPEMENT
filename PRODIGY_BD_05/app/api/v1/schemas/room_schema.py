from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.utils.response import ApiResponse

class RoomCreate(BaseModel):
    title: str
    description: str | None = None
    price_per_night: float
    capacity: int

class RoomResponse(BaseModel):
    id: UUID
    hotel_id: UUID
    title: str
    price_per_night: float
    capacity: int
    is_available: bool
    created_at: datetime

    class Config:
        orm_mode = True

class RoomUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price_per_night: float | None = None
    capacity: int | None = None


class RoomListResponse(ApiResponse[list[RoomResponse]]):
    pass

class RoomDetailResponse(ApiResponse[RoomResponse]):
    pass