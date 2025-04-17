from datetime import date, datetime
from pydantic import BaseModel


class PaymentIn(BaseModel):
    booking_id: int
    method: str


class PaymentOut(BaseModel):
    id: int
    booking_id: int
    invoice_id: int
    method: str
    status: str
    paid_at: datetime | None = None

    model_config = {'from_attributes': True}
