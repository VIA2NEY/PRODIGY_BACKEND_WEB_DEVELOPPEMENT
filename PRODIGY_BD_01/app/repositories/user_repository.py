from uuid import UUID
from typing import Dict
from app.domain.models import User

class UserRepository:
    def __init__(self):
        self.users: Dict[UUID, User] = {}

    def create(self, user: User):
        self.users[user.id] = user
        return user

    def get(self, user_id: UUID):
        return self.users.get(user_id)

    def get_all(self):
        return list(self.users.values())

    def update(self, user_id: UUID, user: User):
        self.users[user_id] = user
        return user

    def delete(self, user_id: UUID):
        return self.users.pop(user_id, None)
