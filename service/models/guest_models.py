from datetime import date

from pydantic import BaseModel

from app.service.models.address_models import AddressOut


class GuestIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    address_id: int

    model_config = {'from_attributes': True}


class GuestOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    address: AddressOut

    model_config = {'from_attributes': True}


class GuestUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    address_id: int


model_config = {'from_attributes': True}
