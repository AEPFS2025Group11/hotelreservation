from datetime import date

from pydantic import BaseModel


class BookingIn(BaseModel):
    guest_id: int
    room_id: int
    check_in: date
    check_out: date
    is_cancelled: bool = False
    total_amount: float

    model_config = {'from_attributes': True}


class BookingOut(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in: date
    check_out: date
    is_cancelled: bool = False
    total_amount: float

    model_config = {'from_attributes': True}


class BookingUpdate(BaseModel):
    room_id: int
    check_in: date
    check_out: date
    is_cancelled: bool = False
    total_amount: float


model_config = {'from_attributes': True}
