from datetime import datetime

from pydantic import BaseModel

from app.util.enums import PaymentStatus


class PaymentIn(BaseModel):
    booking_id: int
    invoice_id: int
    method: str
    amount: float


class PaymentOut(BaseModel):
    id: int
    booking_id: int
    invoice_id: int
    method: str
    status: PaymentStatus
    amount: float
    paid_at: datetime | None = None

    model_config = {'from_attributes': True}
