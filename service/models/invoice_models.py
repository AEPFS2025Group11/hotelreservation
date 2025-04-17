from typing import Optional

from pydantic import BaseModel
from datetime import date

from app.util.enums import InvoiceStatus


class InvoiceOut(BaseModel):
    id: int
    booking_id: int
    issue_date: date
    total_amount: int
    status: InvoiceStatus

    model_config = {'from_attributes': True}


class InvoiceUpdate(BaseModel):
    issue_date: Optional[date] = None
    total_amount: Optional[float] = None
    status: Optional[InvoiceStatus] = None
