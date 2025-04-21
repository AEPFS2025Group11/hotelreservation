from app.database.database import SessionLocal
from app.repository.base_repository import BaseRepository
from app.service.entity.invoice import Invoice


class InvoiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), Invoice)

    def get_by_booking_id(self, booking_id: int) -> Invoice | None:
        return self.db.query(Invoice).filter(Invoice.booking_id == booking_id).first()
