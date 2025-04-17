import logging
from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from app.repository.payment_repository import PaymentRepository
from app.repository.invoice_repository import InvoiceRepository
from app.repository.booking_repository import BookingRepository

from app.service.entity.payment import Payment
from app.service.models.payment_models import PaymentIn, PaymentOut

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PaymentService:
    def __init__(
            self,
            payment_repo: PaymentRepository,
            invoice_repo: InvoiceRepository,
            booking_repo: BookingRepository,
    ):
        self.payment_repo = payment_repo
        self.invoice_repo = invoice_repo
        self.booking_repo = booking_repo

    def create(self, data: PaymentIn) -> PaymentOut:
        logger.info(f"Processing payment for invoice {data.invoice_id} and booking {data.booking_id}")

        invoice = self.invoice_repo.get_by_id(data.invoice_id)
        booking = self.booking_repo.get_by_id(data.booking_id)

        if not invoice or not booking:
            raise HTTPException(status_code=404, detail="Invoice or booking not found")

        payment = Payment(
            booking_id=data.booking_id,
            invoice_id=data.invoice_id,
            method=data.method,
            status="paid",
            paid_at=datetime.now(),
        )

        saved = self.payment_repo.create(payment)
        logger.info(f"Payment recorded for booking {data.booking_id}")
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
