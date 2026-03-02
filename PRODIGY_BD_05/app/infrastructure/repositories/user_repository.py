from app.domain.models.users import User
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db : Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()