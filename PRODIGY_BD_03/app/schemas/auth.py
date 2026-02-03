from pydantic import BaseModel, EmailStr

from app.schemas.response import ApiResponse

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None
    age: int | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDetailResponse(ApiResponse[TokenResponse]):
    pass


class RegisterDetailResponse(ApiResponse[RegisterRequest]):
    pass