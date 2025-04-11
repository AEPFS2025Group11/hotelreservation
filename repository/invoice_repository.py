from app.data_access_layer.database import SessionLocal
from app.data_access_layer.entity.invoice import Invoice


class InvoiceRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Invoice).all()

    def get_by_id(self, invoice_id: int):
        return self.db.query().filter(Invoice.invoice_id == invoice_id).first()
