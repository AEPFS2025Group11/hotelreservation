from app.database.database import SessionLocal
from app.service.entity.invoice import Invoice


class InvoiceRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Invoice).all()

    def get_by_id(self, invoice_id: int):
        return self.db.query().filter(Invoice.invoice_id == invoice_id).first()
