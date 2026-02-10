from app.domain.models.hotels import Hotel
from sqlalchemy.orm import Session

class HotelRepository:

    def create(self, db: Session, hotel: Hotel):
        db.add(hotel)
        db.commit()
        db.refresh(hotel)
        return hotel

    def get_by_owner(self, db: Session, owner_id):
        return db.query(Hotel).filter(Hotel.owner_id == owner_id).all()

    def get_all(self, db: Session):
        return db.query(Hotel).all()

    def get_by_id(self, db: Session, hotel_id):
        return db.query(Hotel).filter(Hotel.id == hotel_id).first()
    
    # def delete(self, hotel: Hotel):
    #     db.delete(hotel)
    #     db.commit()

    def update(self, db: Session, hotel: Hotel):
        db.add(hotel)
        db.commit()
        db.refresh(hotel)
        return hotel