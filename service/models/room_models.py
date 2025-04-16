from pydantic import BaseModel

from app.service.models.hotel_models import HotelOut
from app.service.models.room_type_models import RoomTypeOut


class RoomIn(BaseModel):
    hotel: HotelOut
    room_number: str
    type_id: RoomTypeOut
    price_per_night: float

    model_config = {'from_attributes': True}


class RoomOut(BaseModel):
    room_id: int
    room_number: str
    type: RoomTypeOut
    price_per_night: float

    model_config = {'from_attributes': True}


class RoomUpdate(BaseModel):
    room_number: str
    type_id: RoomTypeOut
    price_per_night: float

    model_config = {'from_attributes': True}
