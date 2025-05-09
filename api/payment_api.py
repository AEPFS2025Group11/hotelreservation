from typing import Optional

from fastapi import APIRouter, Depends

from app.services.models.payment_models import PaymentIn, PaymentOut
from app.services.payment_service import PaymentService, get_payment_service

router = APIRouter(prefix="/api/payments", tags=["payments"])

@router.post("/", response_model=PaymentOut)
async def create_payment(data: PaymentIn, service: PaymentService = Depends(get_payment_service)):
    return service.create(data)


@router.get("/", response_model=list[PaymentOut])
async def get_payments(status: Optional[str] = None, service: PaymentService = Depends(get_payment_service)):
    return service.get_all(status=status)


@router.patch("/{payment_id}/cancel", response_model=PaymentOut)
async def cancel_payment(payment_id: int, service: PaymentService = Depends(get_payment_service)):
    return service.cancel(payment_id)
