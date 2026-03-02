from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.dependencies import get_auth_service_v1
from app.api.v1.schemas.auth_shema import LoginRequest, RegisterDetailResponse, TokenDetailResponse, UserRole
from app.application.services.v1.auth_service import AuthService
from app.utils.response import ApiResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterDetailResponse)
def register(payload: LoginRequest, role: UserRole = UserRole.USER, service : AuthService = Depends(get_auth_service_v1)):
    user = service.register(payload.email, payload.password, role)
    if not user:
        raise HTTPException(
            status_code=400,
            detail={"code": 400, "message": "Email already exists", "data": None},
        )
    
    return RegisterDetailResponse(
        code=201,
        message="User registered successfully",
        data=user,
    )

@router.post("/login", response_model=TokenDetailResponse)
def login(payload: LoginRequest, service : AuthService = Depends(get_auth_service_v1)):
    token = service.login(payload)
    if not token:
        raise HTTPException(
            status_code=401,
            detail={"code": 401, "message": "Login or Password Incorect", "data": None},
        )

    return ApiResponse(
        code=200,
        message="Login successful",
        data={"access_token": token, "token_type": "bearer"},
    )
