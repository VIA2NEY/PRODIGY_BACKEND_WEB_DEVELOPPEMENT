from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

from app.utils.response import ApiResponse

class BookingCreate(BaseModel):
    room_id: UUID
    check_in_date: date
    check_out_date: date

class BookingResponse(BaseModel):
    id: UUID
    user_id: UUID
    room_id: UUID
    check_in_date: date
    check_out_date: date
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    check_in_date: date
    check_out_date: date


class BookingListResponse(ApiResponse[list[BookingResponse]]):
    pass

class BookingDetailResponse(ApiResponse[BookingResponse]):
    pass