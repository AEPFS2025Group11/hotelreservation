from app.entities.room_type import RoomType
from app.repositories.base_repository import BaseRepository


class RoomTypeRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, RoomType)
