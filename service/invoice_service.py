# app/service/invoice_service.py
from datetime import date
from functools import lru_cache

from fastapi import HTTPException
from app.repository.invoice_repository import InvoiceRepository
from app.repository.booking_repository import BookingRepository
from app.service.models.invoice_models import InvoiceOut
from app.service.entity.invoice import Invoice


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
