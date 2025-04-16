from pydantic import BaseModel
from datetime import date


class InvoiceOut(BaseModel):
    id: int
    booking_id: int
    issue_date: date
    total_amount: int

    model_config = {'from_attributes': True}
