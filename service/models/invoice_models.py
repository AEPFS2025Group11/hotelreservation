from typing import Optional

from pydantic import BaseModel
from datetime import date


class InvoiceOut(BaseModel):
    id: int
    booking_id: int
    issue_date: date
    total_amount: int

    model_config = {'from_attributes': True}


class InvoiceUpdate(BaseModel):
    issue_date: Optional[date] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
