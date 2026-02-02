from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.schemas.user import UserCreate, UserDetailResponse, UserListResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter(prefix="/users", tags=["Users"])

user_repo = UserRepository()
user_service = UserService(user_repo)


@router.get("/{user_id}", response_model=UserDetailResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "message": "Resource not found",
                "data": None,
            },
        )
    return UserDetailResponse(code=200, message="OK", data=user.__dict__)


@router.get("/", response_model=UserListResponse)
def get_all_users(db: Session = Depends(get_db)):

    
    users = user_service.get_users(db)
    if not users:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "message": "Resource not found",
                "data": [],
            },
        )
    
    return UserListResponse(code=200, message="OK", data=[user.__dict__ for user in users])

@router.post("/", response_model=UserDetailResponse)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    
    
    user = user_service.create_user(db, **payload.dict())
    return UserDetailResponse(
        code=201,
        message="Utilisateur créé avec succès",
        data=user.__dict__,
    )

@router.put("/{user_id}", response_model=UserDetailResponse)
def update_user(
    user_id: UUID, 
    payload: UserUpdate,
    db: Session = Depends(get_db)
):
    
    
    user = user_service.update_user(db, user_id, payload)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "message": "Resource not found",
                "data": None,
            },
        )
    return UserDetailResponse(code=200, message="Utilisateur mis à jour", data=user.__dict__)

@router.delete("/{user_id}", response_model=UserDetailResponse)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    
    try:
        user_service.delete_user(db, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "code": 404,
                "message": f"Resource not found\n{e}",
                "data": None,
            },
        )
    return UserDetailResponse(code=200, message="User delete with success", data=None)
