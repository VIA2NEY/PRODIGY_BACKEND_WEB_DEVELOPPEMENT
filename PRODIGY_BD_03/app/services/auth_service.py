from sqlalchemy.orm import Session
from app.core.exceptions import raise_exception
from app.domain.models import User
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.auth import RegisterRequest

class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, db: Session, data: RegisterRequest):
        if self.repository.get_by_email(db, data.email):
            return raise_exception(409, f"User with email {data.email} already exists")

        user = User(
            email=data.email,
            # password_hash=get_password_hash(data.password),
            name=data.name,
            age=data.age,
            # role="user",
        )
        return self.repository.create(db, user)

    def login(self, db: Session, email: str, password: str):
        user = self.repository.get_by_email(db, email)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        token = create_access_token({
            "sub": user.email,
            "user_id": user.id,
            "role": user.role,
        })

        return token
