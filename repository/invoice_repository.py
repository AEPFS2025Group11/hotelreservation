from app.business_layer.entity.invoice import Invoice
from app.util.database import SessionLocal


class InvoiceRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Invoice).all()

    def get_by_id(self, invoice_id: int):
        return self.db.query().filter(Invoice.invoice_id == invoice_id).first()
