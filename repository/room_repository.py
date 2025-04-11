from app.data_access_layer.database import SessionLocal
from app.data_access_layer.entity.room import Room


class RoomRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Room).all()

    def get_by_id(self, room_id: int):
        return self.db.query().filter(Room.room_id == room_id).first()
