from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.dependencies import get_auth_service_v1
from app.api.v1.schemas.auth_shema import LoginRequest, RegisterDetailResponse, TokenDetailResponse, UserRole
from app.infrastructure.database.session import get_db
from sqlalchemy.orm import Session
from app.utils.response import ApiResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterDetailResponse)
def register(payload: LoginRequest, role: UserRole = UserRole.USER, service=Depends(get_auth_service_v1), db: Session = Depends(get_db)):
    user = service.register(db, payload.email, payload.password, role)
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
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = get_auth_service_v1().login(db, payload)
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
