from fastapi import HTTPException

from app.repository.room_repository import RoomRepository
from app.repository.room_type import RoomTypeRepository
from app.service.entity.room import Room
from app.service.models.room_models import RoomOut, RoomUpdate, RoomIn


class RoomService:
    def __init__(self):
        self.room_type_repo = RoomTypeRepository()
        self.room_repo = RoomRepository()

    def get_all(self) -> list[RoomOut]:
        rooms = self.room_repo.get_all()
        if rooms is None:
            raise HTTPException(status_code=404, detail="No rooms found")
        return [RoomOut.model_validate(r) for r in rooms]

    def get_by_id(self, room_id) -> RoomOut:
        room = self.room_repo.get_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=404, detail=f"Room with id {room_id} not found")
        return RoomOut.model_validate(room)

    def create(self, room: RoomIn) -> RoomOut:
        room_type = self.room_type_repo.get_by_id(room.type_id)
        if room_type is None:
            raise HTTPException(status_code=404, detail="Room type not found")
        room = Room(room_number=room.room_number, type_id=room.type_id, hotel_id=room.hotel_id,
                    price_per_night=room.price_per_night)
        room = self.room_repo.create(room)
        if room is None:
            raise HTTPException(status_code=500, detail=f"Ups something went wrong")
        return RoomOut.model_validate(room)

    def update(self, room_id: int, data: RoomUpdate) -> RoomOut:
        print('test')
        room_entity = self.room_repo.get_by_id(room_id)
        if room_entity is None:
            raise HTTPException(status_code=404, detail="Room not found")
        if data.room_number is not None:
            room_entity.room_number = data.room_number
        if data.price_per_night is not None:
            room_entity.price_per_night = data.price_per_night
        if data.type_id is not None:
            room_entity.type_id = data.type_id
        updated_room = self.room_repo.update(room_entity)
        return RoomOut.model_validate(updated_room)

    def delete(self, room_id: int) -> RoomOut:
        room = self.room_repo.get_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=404, detail=f"Room with id {room_id} not found")
        deleted_room = self.room_repo.delete(room_id)
        return deleted_room
