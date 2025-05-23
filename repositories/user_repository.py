from app.database.database import SessionLocal
from app.repositories.base_repository import BaseRepository
from app.entities.user import User


class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, User)
