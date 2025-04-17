from app.database.database import SessionLocal
from app.repository.base_repository import BaseRepository
from app.service.entity.payment import Payment


class PaymentRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), Payment)
