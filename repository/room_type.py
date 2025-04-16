from app.database.database import SessionLocal
from app.service.entity.room_type import RoomType


class RoomTypeRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(RoomType).all()

    def get_by_id(self, type_id: int):
        return self.db.query(RoomType).filter(RoomType.id == type_id).first()
