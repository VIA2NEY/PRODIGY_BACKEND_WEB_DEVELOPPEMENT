from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.schemas.response import ApiResponse

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    age: int



# Ajout d'un schéma de réponse spécifique
class UserListResponse(ApiResponse[list[UserResponse]]):
    pass

class UserDetailResponse(ApiResponse[UserResponse]):
    pass