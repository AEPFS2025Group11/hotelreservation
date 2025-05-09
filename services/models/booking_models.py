from datetime import date

from pydantic import BaseModel

from app.services.models.invoice_models import InvoiceOut
from app.services.models.room_models import RoomOut
from app.services.models.user_models import UserModel


class BookingIn(BaseModel):
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    is_cancelled: bool = False
    total_amount: float

    model_config = {'from_attributes': True}


class BookingOut(BaseModel):
    id: int
    invoice: InvoiceOut
    user: UserModel
    room: RoomOut
    check_in: date
    check_out: date
    is_cancelled: bool = False
    is_paid: bool
    total_amount: float

    model_config = {'from_attributes': True}


class BookingUpdate(BaseModel):
    room_id: int
    check_in: date
    check_out: date
    is_cancelled: bool = False
    total_amount: float


model_config = {'from_attributes': True}
