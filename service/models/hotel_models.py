from typing import Optional

from pydantic import BaseModel

from app.service.models.address_models import AddressOut


class HotelIn(BaseModel):
    name: str
    stars: int
    address_id: int

    model_config = {'from_attributes': True}


class HotelOut(BaseModel):
    hotel_id: int
    name: str
    stars: int
    address: AddressOut

    model_config = {'from_attributes': True}


class HotelUpdate(BaseModel):
    name: Optional[str] = None
    stars: Optional[int] = None

    model_config = {'from_attributes': True}
