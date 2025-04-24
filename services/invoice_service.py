import logging
from datetime import date

from fastapi import HTTPException

from app.repositories.booking_repository import BookingRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.entities.invoice import Invoice
from app.services.models.invoice_models import InvoiceOut, InvoiceUpdate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class InvoiceService:
    def __init__(self, invoice_repo: InvoiceRepository, booking_repo: BookingRepository):
        self.invoice_repo = invoice_repo
        self.booking_repo = booking_repo

    def create(self, booking_id: int) -> InvoiceOut:
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if booking.invoice:
            raise HTTPException(status_code=400, detail="Invoice already exists")

        invoice = Invoice(
            booking_id=booking.id,
            issue_date=date.today(),
            total_amount=booking.total_amount
        )
        saved = self.invoice_repo.create(invoice)
        return InvoiceOut.model_validate(saved)

    def get_all(self) -> list[InvoiceOut]:
        logger.info("Fetching all invoices")
        invoices = self.invoice_repo.get_all()
        logger.info(f"{len(invoices)} invoice(s) found")
        return [InvoiceOut.model_validate(i) for i in invoices]

    def get_by_id(self, invoice_id: int) -> InvoiceOut:
        logger.info(f"Fetching invoice ID {invoice_id}")
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            logger.warning(f"Invoice ID {invoice_id} not found")
            raise HTTPException(status_code=404, detail="Invoice not found")
        return InvoiceOut.model_validate(invoice)

    def update(self, invoice_id: int, data: InvoiceUpdate) -> InvoiceOut:
        logger.info(f"Updating invoice ID {invoice_id}")
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            logger.warning(f"Invoice ID {invoice_id} not found for update")
            raise HTTPException(status_code=404, detail="Invoice not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(invoice, field, value)

        updated_invoice = self.invoice_repo.update(invoice)
        logger.info(f"Invoice ID {invoice_id} updated successfully")
        return InvoiceOut.model_validate(updated_invoice)
