from app.api.v1.schemas.auth_shema import LoginRequest
from app.core.exceptions import raise_exception
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.domain.models.users import User
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, db: Session, email: str, password: str, role: str):
        if self.user_repo.get_by_email(db, email):
            raise_exception(409, f"User with email {email} already exists")

        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            role=role
        )
        return self.user_repo.create(db, user)


    def login(self, db: Session, payload: LoginRequest):
        user = self.user_repo.get_by_email(db, payload.email)
        if not user:
            return None

        if not user or not verify_password(payload.password, user.hashed_password):
            return None

        token = create_access_token({
            "sub": user.email,
            "user_id": str(user.id),
            "role": user.role,
        })

        return token