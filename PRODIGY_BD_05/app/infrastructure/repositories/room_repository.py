from sqlalchemy import and_
from app.domain.models.booking import Booking
from app.domain.models.rooms import Room
from sqlalchemy.orm import Session


class RoomRepository:

    def create(self, db: Session, room: Room):
        db.add(room)
        db.commit()
        db.refresh(room)
        return room
    
    def update(self, db: Session, room: Room):
        db.add(room)
        db.commit()
        db.refresh(room)
        return room
    
    def delete(self, db: Session, room: Room):
        db.delete(room)
        db.commit()

    def get_all_available_rooms(self, db: Session):
        return db.query(Room).filter(Room.is_available == True).all()

    def get_by_id(self, db: Session, room_id):
        return db.query(Room).filter(Room.id == room_id).first()
    
    def get_all_rooms_by_hotel_id(self, db: Session, hotel_id):
        return db.query(Room).filter(Room.hotel_id == hotel_id).all()
    
    def get_available_rooms_by_hotel_id(self, db: Session, hotel_id):
        return db.query(Room).filter(Room.hotel_id == hotel_id, Room.is_available == True).all()
    
    def get_booked_rooms_by_hotel_id(self, db: Session, hotel_id):
        return db.query(Room).filter(Room.hotel_id == hotel_id, Room.is_available == False).all()
    
    def get_all_rooms(self, db: Session):
        return db.query(Room).all()
    
    
    def get_available_by_date(self, db: Session, check_in, check_out):
        """
        Get all available rooms for a given date range.

        Args:
            db (Session): The database session.
            check_in (date): The start date of the range.
            check_out (date): The end date of the range.

        Returns:
            List[Room]: A list of available rooms.

        Le symbole ~ signifie "NOT" (non). On cherche 
        les chambres qui n'ont aucune réservation (any) 
        correspondant aux critères entre parenthèses.
        
        """
        return db.query(Room).filter(
            Room.is_available == True,
            ~Room.bookings.any(
                and_(
                    Booking.check_in_date < check_out,
                    Booking.check_out_date > check_in,
                    Booking.status == "confirmed"
                )
            )
        ).all()