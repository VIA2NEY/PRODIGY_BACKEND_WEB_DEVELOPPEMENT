from sqlalchemy.orm import Session
from app.domain.models import User

class UserRepository:

    def create(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get(self, db: Session, user_id: str):
        return db.query(User).filter(User.id == str(user_id)).first()

    def get_all(self, db: Session):
        return db.query(User).all()

    def update(self, db: Session, user: User):
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user: User):
        db.delete(user)
        db.commit()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()