from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    age: int
