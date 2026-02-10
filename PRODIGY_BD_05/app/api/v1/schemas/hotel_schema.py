from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.utils.response import ApiResponse

class HotelCreate(BaseModel):
    name: str
    description: str | None = None
    address: str

class HotelUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    address: str | None = None

class HotelResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    address: str
    owner_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True



class HotelListResponse(ApiResponse[list[HotelResponse]]):
    pass

class HotelDetailResponse(ApiResponse[HotelResponse]):
    pass