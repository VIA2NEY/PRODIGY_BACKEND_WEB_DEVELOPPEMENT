from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

from app.utils.response import ApiResponse

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str



class UserListResponse(ApiResponse[list[UserResponse]]):
    pass

class UserDetailResponse(ApiResponse[UserResponse]):
    pass