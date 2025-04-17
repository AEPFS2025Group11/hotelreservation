from app.database.database import SessionLocal
from app.repository.base_repository import BaseRepository
from app.service.entity.room_type import RoomType


class RoomTypeRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), RoomType)
