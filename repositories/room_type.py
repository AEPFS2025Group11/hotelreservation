from app.database.database import SessionLocal
from app.repositories.base_repository import BaseRepository
from app.entities import RoomType


class RoomTypeRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), RoomType)
