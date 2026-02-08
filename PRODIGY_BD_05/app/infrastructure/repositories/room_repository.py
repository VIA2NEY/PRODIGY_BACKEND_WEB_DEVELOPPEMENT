from app.domain.models.rooms import Room


class RoomRepository:
    def __init__(self, db):
        self.db = db

    def create(self, room: Room):
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room
    
    def update(self, room: Room):
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room
    
    def delete(self, room: Room):
        self.db.delete(room)
        self.db.commit()

    def get_all_available_rooms(self):
        return self.db.query(Room).filter(Room.is_available == True).all()

    def get_by_id(self, room_id):
        return self.db.query(Room).filter(Room.id == room_id).first()
    
    def get_all_rooms_by_hotel_id(self, hotel_id):
        return self.db.query(Room).filter(Room.hotel_id == hotel_id).all()
    
    def get_available_rooms_by_hotel_id(self, hotel_id):
        return self.db.query(Room).filter(Room.hotel_id == hotel_id, Room.is_available == True).all()
    
    def get_booked_rooms_by_hotel_id(self, hotel_id):
        return self.db.query(Room).filter(Room.hotel_id == hotel_id, Room.is_available == False).all()
    
    def get_all_rooms(self):
        return self.db.query(Room).all()