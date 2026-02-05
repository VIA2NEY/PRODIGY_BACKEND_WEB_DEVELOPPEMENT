from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.auth import RegisterDetailResponse, RegisterRequest, LoginRequest, TokenDetailResponse, TokenResponse
from app.schemas.response import ApiResponse
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

repository = UserRepository()
service = AuthService(repository)

@router.post("/register", response_model=RegisterDetailResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = service.register(db, payload)
    if not user:
        raise HTTPException(
            status_code=400,
            detail={"code": 400, "message": "Email already exists", "data": None},
        )
    
    return RegisterDetailResponse(
        code=201,
        message="User registered successfully",
        data=user.__dict__,
    )


@router.post("/login", response_model=TokenDetailResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = service.login(db, payload.email, payload.password)
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
