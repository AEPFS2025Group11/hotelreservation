from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.entity.room import Room


class RoomRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Room).all()

    def get_by_id(self, room_id: int):
        return self.db.query(Room).filter(Room.room_id == room_id).first()

    def get_by_hotel_id(self, hotel_id) -> list[Room]:
        return self.db.query(Room).filter(hotel_id == Room.hotel_id).options(joinedload(Room.type)).all()
