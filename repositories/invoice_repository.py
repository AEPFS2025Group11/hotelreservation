import logging

from app.entities.invoice import Invoice
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class InvoiceRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Invoice)

    def get_by_booking_id(self, booking_id: int) -> Invoice | None:
        return self.db.query(Invoice).filter(Invoice.booking_id == booking_id).first()

