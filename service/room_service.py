import logging
from datetime import date
from typing import Optional

from fastapi import HTTPException

from app.repository.room_repository import RoomRepository
from app.repository.room_type import RoomTypeRepository
from app.service.entity.room import Room
from app.service.models.room_models import RoomOut, RoomUpdate, RoomIn
from app.util.dynamic_pricing import calculate_dynamic_price

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RoomService:
    def __init__(self, room_repo: RoomRepository, room_type_repo: RoomTypeRepository):
        self.room_repo = room_repo
        self.room_type_repo = room_type_repo

    def get_all(self, city: Optional[str] = None,
                capacity: Optional[int] = None,
                check_in: Optional[date] = None,
                check_out: Optional[date] = None) -> list[RoomOut]:

        logger.info(f"Fetching rooms with filters: city='{city}', capacity={capacity}, "
                    f"check_in={check_in}, check_out={check_out}")

        if check_in and check_out and check_in > check_out:
            raise HTTPException(status_code=400, detail="Check-out date must be after check-in date")

        rooms = self.room_repo.get_all(city, capacity, check_in, check_out)

        if not rooms:
            raise HTTPException(status_code=404, detail="No rooms found")

        room_dtos = []
        nights = (check_out - check_in).days if check_in and check_out else None

        for room in rooms:
            dto = RoomOut.model_validate(room)

            dynamic_price = calculate_dynamic_price(dto.price_per_night, check_in)
            dto.dynamic_price_per_night = dynamic_price

            if nights:
                dto.total_price = dynamic_price * nights

            room_dtos.append(dto)

        return room_dtos

    def get_by_id(self, room_id: int, check_in: Optional[date] = None, check_out: Optional[date] = None) -> RoomOut:
        logger.info(f"Fetching room by ID: {room_id}")
        room = self.room_repo.get_by_id(room_id)
        if room is None:
            logger.warning(f"Room with ID {room_id} not found")
            raise HTTPException(status_code=404, detail=f"Room with id {room_id} not found")

        room_dto = RoomOut.model_validate(room)

        dynamic_price = calculate_dynamic_price(room_dto.price_per_night, check_in)
        room_dto.dynamic_price_per_night = dynamic_price

        if check_in and check_out:
            nights = (check_out - check_in).days
            room_dto.total_price = dynamic_price * nights
        else:
            room_dto.total_price = None

        return room_dto

    def create(self, room: RoomIn) -> RoomOut:
        logger.info(f"Creating new room with data: {room.model_dump()}")
        room_type = self.room_type_repo.get_by_id(room.type_id)
        if room_type is None:
            logger.warning(f"Room type with ID {room.type_id} not found")
            raise HTTPException(status_code=404, detail="Room type not found")
        room_entity = Room(**room.model_dump())
        created_room = self.room_repo.create(room_entity)
        if created_room is None:
            logger.error("Room creation failed due to unknown internal error")
            raise HTTPException(status_code=500, detail="An error occurred while creating the room")
        logger.info(f"Room created with ID {created_room.id}")
        return RoomOut.model_validate(created_room)

    def update(self, room_id: int, data: RoomUpdate) -> RoomOut:
        logger.info(f"Updating room ID {room_id} with fields: {data.model_dump()}")
        room_entity = self.room_repo.get_by_id(room_id)
        if room_entity is None:
            logger.warning(f"Room with ID {room_id} not found for update")
            raise HTTPException(status_code=404, detail="Room not found")

        if data.room_number is not None:
            room_entity.room_number = data.room_number
        if data.price_per_night is not None:
            room_entity.price_per_night = data.price_per_night
        if data.type_id is not None:
            room_entity.type_id = data.type_id

        updated_room = self.room_repo.update(room_entity)
        logger.info(f"Room ID {room_id} updated successfully")
        return RoomOut.model_validate(updated_room)

    def delete(self, room_id: int) -> RoomOut:
        logger.info(f"Deleting room with ID: {room_id}")
        room = self.room_repo.get_by_id(room_id)
        if room is None:
            logger.warning(f"Room with ID {room_id} not found for deletion")
            raise HTTPException(status_code=404, detail=f"Room with id {room_id} not found")
        deleted_room = self.room_repo.delete(room_id)
        logger.info(f"Room with ID {room_id} successfully deleted")
        return RoomOut.model_validate(deleted_room)
