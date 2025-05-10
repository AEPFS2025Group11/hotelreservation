import logging
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.entities.payment import Payment
from app.repositories.booking_repository import BookingRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.payment_repository import PaymentRepository
from app.services.models.payment_models import PaymentIn, PaymentOut
from app.util.enums import PaymentStatus, InvoiceStatus

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PaymentService:
    def __init__(
            self,
            db: Session
    ):
        self.payment_repo = PaymentRepository(db=db)
        self.invoice_repo = InvoiceRepository(db=db)
        self.booking_repo = BookingRepository(db=db)

    def create(self, data: PaymentIn) -> PaymentOut:
        logger.info(f"Processing payment for invoice {data.invoice_id} and booking {data.booking_id}")

        invoice = self.invoice_repo.get_by_id(data.invoice_id)
        booking = self.booking_repo.get_by_id(data.booking_id)

        if not invoice or not booking:
            raise HTTPException(status_code=404, detail="Invoice oder Buchung konnte nicht gefunden werden.")

        if booking.is_cancelled:
            logger.warning(f"Payment rejected: Booking {booking.id} is cancelled")
            raise HTTPException(status_code=400, detail="Stornierte Buchung kann nicht bezahlt werden.")

        payments_before = self.payment_repo.get_by_invoice_id(invoice.id)
        already_paid = sum(p.amount for p in payments_before if p.status == PaymentStatus.PAID)
        if already_paid >= invoice.total_amount:
            logger.info(f"Rechnung wurde bereits bezahlt")
            raise HTTPException(status_code=400, detail="Rechnung bereits bezahlt.")

        payment = Payment(
            booking_id=data.booking_id,
            invoice_id=data.invoice_id,
            method=data.method,
            status=PaymentStatus.PAID,
            paid_at=datetime.now(),
            amount=data.amount
        )
        saved = self.payment_repo.create(payment)
        logger.info(f"Payment recorded for booking {data.booking_id}")

        payments_after = payments_before + [saved]
        total_paid = sum(p.amount for p in payments_after if p.status == PaymentStatus.PAID)

        if total_paid >= invoice.total_amount:
            invoice.status = InvoiceStatus.PAID
            self.invoice_repo.update(invoice)
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
            raise HTTPException(status_code=404, detail="Zahlung konnte nicht gefunden werden.")

        payment.status = "cancelled"
        payment.paid_at = None
        updated = self.payment_repo.update(payment)

        logger.info(f"Payment ID {payment_id} cancelled")
        return PaymentOut.model_validate(updated)


def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(db=db)
