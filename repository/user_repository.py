from app.database.database import SessionLocal
from app.repository.base_repository import BaseRepository
from app.service.entity.user import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), User)
