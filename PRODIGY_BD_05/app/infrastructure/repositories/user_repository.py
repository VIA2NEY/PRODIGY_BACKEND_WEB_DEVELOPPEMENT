from app.domain.models.users import User
from sqlalchemy.orm import Session

class UserRepository:

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def delete(self, db: Session, user: User):
        db.delete(user)
        db.commit()