from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.service.models.address_models import AddressOut


class GuestIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    address_id: int

    model_config = {'from_attributes': True}


class GuestOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    address: AddressOut

    model_config = {'from_attributes': True}


class GuestUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    address_id: int


model_config = {'from_attributes': True}
