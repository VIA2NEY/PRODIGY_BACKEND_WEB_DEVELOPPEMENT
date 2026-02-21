from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, field_validator
from uuid import UUID
from datetime import date, datetime

from app.utils.response import ApiResponse

class BookingCreate(BaseModel):
    room_id: UUID
    check_in_date: date
    check_out_date: date

    @field_validator("check_in_date", "check_out_date")
    @classmethod
    def dates_cannot_be_past(cls, value):
        if value < date.today():
            raise HTTPException(
                status_code=422,
                detail={"code": 422, "message": f"Dates cannot be in the past, try again from {date.today()} ", "data": None},
            )
        return value

class BookingResponse(BaseModel):
    id: UUID
    user_id: UUID
    room_id: UUID
    check_in_date: date
    check_out_date: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BookingUpdate(BaseModel):
    check_in_date: date
    check_out_date: date


class BookingListResponse(ApiResponse[list[BookingResponse]]):
    pass

class BookingDetailResponse(ApiResponse[BookingResponse]):
    pass