from typing import Optional

from pydantic import BaseModel

from app.services.models.facility_models import FacilityOut
from app.services.models.hotel_models import HotelOut
from app.services.models.room_type_models import RoomTypeOut


class RoomIn(BaseModel):
    hotel_id: int
    room_number: str
    type_id: int
    facility_ids: list[int]
    price_per_night: float

    model_config = {'from_attributes': True}


class RoomOut(BaseModel):
    id: int
    room_number: str
    hotel: HotelOut
    type: RoomTypeOut
    facilities: list[FacilityOut] = []
    price_per_night: float
    dynamic_price_per_night: Optional[float] = None
    total_price: Optional[float] = None

    model_config = {'from_attributes': True}


class RoomUpdate(BaseModel):
    room_number: str
    type_id: int
    facility_ids: list[int]
    price_per_night: float

    model_config = {'from_attributes': True}
