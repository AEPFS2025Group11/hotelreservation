from typing import Optional

from pydantic import BaseModel

from app.services.models.address_models import AddressOut
from app.services.models.hotel_models import HotelOut


class RoomTypeIn(BaseModel):
    description: str
    max_guests: int

    model_config = {'from_attributes': True}


class RoomTypeOut(BaseModel):
    id: int
    description: str
    max_guests: int

    model_config = {'from_attributes': True}


class RoomTypeUpdate(BaseModel):
    description: str
    max_guests: int

    model_config = {'from_attributes': True}
