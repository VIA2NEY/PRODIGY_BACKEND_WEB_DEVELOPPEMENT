from app.domain.models.hotels import Hotel
from sqlalchemy.orm import Session

class HotelRepository:
    def __init__(self, db : Session):
        self.db = db

    def create(self, hotel: Hotel):
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def get_by_owner(self, owner_id):
        return self.db.query(Hotel).filter(Hotel.owner_id == owner_id).all()

    def get_all(self):
        return self.db.query(Hotel).all()

    def get_by_id(self, hotel_id):
        return self.db.query(Hotel).filter(Hotel.id == hotel_id).first()
    
    # def delete(self, hotel: Hotel):
    #     db.delete(hotel)
    #     db.commit()

    def update(self, hotel: Hotel):
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)
        return hotel