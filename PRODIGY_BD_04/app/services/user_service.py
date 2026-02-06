from typing import Optional
from app.cache.cache_service import CacheService
from sqlalchemy.orm import Session
from app.core.exceptions import raise_exception
from app.repositories.user_repository import UserRepository
from app.domain.models import User
from app.schemas.user import UserUpdate
from app.core.config import settings

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
        
        CacheService.delete("users:all")
        return self.repository.create(db, user)

    def get_user(self, db: Session, user_id: str):
        return self.repository.get(db, user_id)

    # def get_users(self, db: Session):
    #     return self.repository.get_all(db)
    
    def get_users(self, db: Session):
        cache_key = "users:all"

        # 1️⃣ Essayer le cache
        cached_users = CacheService.get(cache_key)
        if cached_users:
            return cached_users

        # 2️⃣ Sinon DB
        users = self.repository.get_all(db)

        users_data = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
            }
            for user in users
        ]

        # 3️⃣ Sauvegarde cache
        CacheService.set(
            cache_key,
            users_data,
            settings.REDIS_TTL_USERS
        )

        return users

    def update_user(self, db: Session, user_id: str, data: UserUpdate) -> Optional[User]:
        user = self.repository.get(db, user_id)
        if not user:
            return None
        
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)

        
        CacheService.delete("users:all")
        return self.repository.update(db, user)

    def delete_user(self, db: Session, user_id: str):
        user = self.repository.get(db, user_id)
        if not user:
            return raise_exception(404, "Resource not found")
        
        CacheService.delete("users:all")
        self.repository.delete(db, user)
        # return user

    def get_by_email(self, db: Session, email: str):
        return self.repository.get_by_email(db, email)