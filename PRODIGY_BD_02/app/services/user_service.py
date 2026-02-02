# app/services/user_service.py
from uuid import uuid4, UUID
from app.repositories.user_repository import UserRepository
from app.domain.models import User

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, name: str, email: str, age: int):
        user = User(uuid4(), name, email, age)
        return self.repository.create(user)

    def get_user(self, user_id: UUID):
        return self.repository.get(user_id)

    def get_users(self):
        return self.repository.get_all()

    def update_user(self, user_id: UUID, data: dict):
        user = self.repository.get(user_id)
        if not user:
            return None

        updated = User(
            id=user.id,
            name=data.get("name", user.name),
            email=data.get("email", user.email),
            age=data.get("age", user.age),
        )
        return self.repository.update(user_id, updated)

    def delete_user(self, user_id: UUID):
        return self.repository.delete(user_id)
