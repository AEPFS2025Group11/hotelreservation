from typing import Optional

from fastapi import APIRouter, Depends
from functools import lru_cache

from app.repository.booking_repository import BookingRepository
from app.repository.invoice_repository import InvoiceRepository
from app.repository.payment_repository import PaymentRepository
from app.service.payment_service import PaymentService
from app.service.models.payment_models import PaymentIn, PaymentOut

router = APIRouter(prefix="/api/payments", tags=["payments"])


@lru_cache()
def get_payment_service() -> PaymentService:
    return PaymentService(
        payment_repo=PaymentRepository(),
        invoice_repo=InvoiceRepository(),
        booking_repo=BookingRepository()
    )


@router.post("/", response_model=PaymentOut)
async def pay(data: PaymentIn, service: PaymentService = Depends(get_payment_service)):
    return service.create(data)


@router.get("/", response_model=list[PaymentOut])
async def get_all_payments(status: Optional[str] = None, service: PaymentService = Depends(get_payment_service)):
    return service.get_all(status=status)


@router.patch("/{payment_id}/cancel", response_model=PaymentOut)
async def cancel_payment(payment_id: int, service: PaymentService = Depends(get_payment_service)):
    return service.cancel(payment_id)
