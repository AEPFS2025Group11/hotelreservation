from app.business_layer.entity.room_type import RoomType
from app.util.database import SessionLocal


class RoomTypeRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(RoomType).all()

    def get_by_id(self, type_id: int):
        return self.db.query().filter(RoomType.type_id == type_id).first()
