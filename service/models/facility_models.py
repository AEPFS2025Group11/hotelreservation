from typing import Optional

from pydantic import BaseModel

from app.service.models.address_models import AddressOut
from app.service.models.hotel_models import HotelOut


class FacilityIn(BaseModel):
    facility_name: str

    model_config = {'from_attributes': True}


class FacilityOut(BaseModel):
    facility_id: int
    facility_name: str

    model_config = {'from_attributes': True}


class FacilityUpdate(BaseModel):
    facility_name: str

    model_config = {'from_attributes': True}
