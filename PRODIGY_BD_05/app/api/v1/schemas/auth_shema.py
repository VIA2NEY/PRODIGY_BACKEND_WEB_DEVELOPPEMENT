from pydantic import BaseModel, EmailStr

from app.api.v1.schemas.user_schema import UserResponse
from app.utils.response import ApiResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDetailResponse(ApiResponse[TokenResponse]):
    pass


class RegisterDetailResponse(ApiResponse[UserResponse]):
    pass