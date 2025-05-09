from app.database.database import SessionLocal
from app.repositories.base_repository import BaseRepository
from app.entities.payment import Payment


class PaymentRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Payment)

    def get_by_invoice_id(self, invoice_id: int) -> list[Payment]:
        return self.db.query(Payment).filter(Payment.invoice_id == invoice_id).all()
