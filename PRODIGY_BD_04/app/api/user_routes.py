from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.core.security import get_current_user, require_roles
from app.schemas.user import UserDetailResponse, UserListResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter(prefix="/users", tags=["Users"])

user_repo = UserRepository()
user_service = UserService(user_repo)


@router.get("/profile", response_model=UserDetailResponse)
def profile(db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]

    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "message": "User not found",
                "data": None,
            },
        )

    return UserDetailResponse(
        code=200,
        message="OK",
        data=user.__dict__,
    )

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
# def get_all_users(db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "owner"))):

    
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
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin")),
):
    
    user_service.delete_user(db, user_id)
    
    return UserDetailResponse(code=200, message="User delete with success", data=None)
