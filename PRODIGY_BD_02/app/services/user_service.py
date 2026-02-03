from typing import Optional
from sqlalchemy.orm import Session
from app.core.exceptions import raise_exception
from app.repositories.user_repository import UserRepository
from app.domain.models import User
from app.schemas.user import UserUpdate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, db: Session, name: str, email: str, age: int):
        existing_user = self.repository.get_by_email(db, email)
        if existing_user:
            return raise_exception(409, f"User with email {email} already exists") 

        user = User(
            name=name,
            email=email,
            age=age
        )
        return self.repository.create(db, user)

    def get_user(self, db: Session, user_id: str):
        return self.repository.get(db, user_id)

    def get_users(self, db: Session):
        return self.repository.get_all(db)

    def update_user(self, db: Session, user_id: str, data: UserUpdate) -> Optional[User]:
        user = self.repository.get(db, user_id)
        if not user:
            return None
        
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)

        return self.repository.update(db, user)

    def delete_user(self, db: Session, user_id: str):
        user = self.repository.get(db, user_id)
        if not user:
            return raise_exception(404, "Resource not found")

        self.repository.delete(db, user)
        # return user

    def get_by_email(self, db: Session, email: str):
        return self.repository.get_by_email(db, email)