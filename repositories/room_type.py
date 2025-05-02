from app.database.database import SessionLocal
from app.entities.room_type import RoomType
from app.repositories.base_repository import BaseRepository


class RoomTypeRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), RoomType)
