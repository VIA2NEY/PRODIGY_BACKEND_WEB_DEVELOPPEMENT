from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.response import ApiResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

repo = UserRepository()
service = UserService(repo)


@router.get("/{user_id}", response_model=ApiResponse)
def get_user(user_id: UUID):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "message": "Resource not found",
                "data": None,
            },
        )
    return ApiResponse(code=200, message="OK", data=user.__dict__)


@router.post("/", response_model=ApiResponse)
def create_user(payload: UserCreate):
    user = service.create_user(**payload.dict())
    return ApiResponse(
        code=201,
        message="Utilisateur créé avec succès",
        data=user.__dict__,
    )

@router.put("/{user_id}", response_model=ApiResponse)
def update_user(user_id: UUID, payload: UserUpdate):
    user = service.update_user(user_id, payload.dict())
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "message": "Resource not found",
                "data": None,
            },
        )
    return ApiResponse(code=200, message="Utilisateur mis à jour", data=user.__dict__)

@router.delete("/{user_id}", response_model=ApiResponse)
def delete_user(user_id: UUID):
    user = service.delete_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "message": "Resource not found",
                "data": None,
            },
        )
    return ApiResponse(code=200, message="Utilisateur supprimé", data=None)
