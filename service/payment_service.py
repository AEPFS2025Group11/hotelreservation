import logging
from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from app.repository.payment_repository import PaymentRepository
from app.service.booking_service import BookingService
from app.service.entity.payment import Payment
from app.service.invoice_service import InvoiceService
from app.service.models.invoice_models import InvoiceUpdate
from app.service.models.payment_models import PaymentIn, PaymentOut

STATUS_PAID = "paid"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PaymentService:
    def __init__(
            self,
            payment_repo: PaymentRepository,
            invoice_service: InvoiceService,
            booking_service: BookingService,
    ):
        self.payment_repo = payment_repo
        self.invoice_service = invoice_service
        self.booking_service = booking_service

    def create(self, data: PaymentIn) -> PaymentOut:
        logger.info(f"Processing payment for invoice {data.invoice_id} and booking {data.booking_id}")

        invoice = self.invoice_service.get_by_id(data.invoice_id)
        booking = self.booking_service.get_by_id(data.booking_id)

        if not invoice or not booking:
            raise HTTPException(status_code=404, detail="Invoice or booking not found")

        payment = Payment(
            booking_id=data.booking_id,
            invoice_id=data.invoice_id,
            method=data.method,
            status=STATUS_PAID,
            paid_at=datetime.now(),
            amount=data.amount
        )
        saved = self.payment_repo.create(payment)
        logger.info(f"Payment recorded for booking {data.booking_id}")

        all_payments = self.payment_repo.get_by_invoice_id(invoice.id)
        total_paid = sum(p.amount for p in all_payments if p.status == STATUS_PAID)

        if total_paid >= invoice.total_amount:
            invoice_update = InvoiceUpdate(status=STATUS_PAID)
            self.invoice_service.update(invoice.id, invoice_update)
            logger.info(f"Invoice {invoice.id} marked as paid")

        return PaymentOut.model_validate(saved)

    def get_all(self, status: Optional[str] = None) -> list[PaymentOut]:
        logger.info("Fetching all payments")
        payments = self.payment_repo.get_all()

        if status:
            payments = [p for p in payments if p.status == status]

        return [PaymentOut.model_validate(p) for p in payments]

    def cancel(self, payment_id: int) -> PaymentOut:
        logger.info(f"Cancelling payment ID {payment_id}")
        payment = self.payment_repo.get_by_id(payment_id)

        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        payment.status = "cancelled"
        payment.paid_at = None
        updated = self.payment_repo.update(payment)

        logger.info(f"Payment ID {payment_id} cancelled")
        return PaymentOut.model_validate(updated)
