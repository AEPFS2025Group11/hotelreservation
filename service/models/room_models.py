from pydantic import BaseModel

from app.service.models.room_type_models import RoomTypeOut


class RoomIn(BaseModel):
    hotel_id: int
    room_number: str
    type_id: int
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
    type_id: int
    price_per_night: float

    model_config = {'from_attributes': True}
