from datetime import date
from functools import lru_cache
from typing import Optional

from fastapi import APIRouter, Depends

from app.repository.room_repository import RoomRepository
from app.repository.room_type import RoomTypeRepository
from app.service.models.room_models import RoomOut, RoomIn, RoomUpdate
from app.service.room_service import RoomService

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


@lru_cache()
def get_room_service() -> RoomService:
    room_repo = RoomRepository()
    room_type_repo = RoomTypeRepository()
    return RoomService(room_repo=room_repo, room_type_repo=room_type_repo)


@router.get("/", response_model=list[RoomOut])
async def get_rooms(
        city: Optional[str] = None,
        capacity: Optional[int] = None,
        check_in: Optional[date] = None,
        check_out: Optional[date] = None,
        service: RoomService = Depends(get_room_service)
) -> list[RoomOut]:
    return service.get_all(city, capacity, check_in, check_out)


@router.get("/{room_id}", response_model=RoomOut)
async def get_room(
        room_id: int,
        service: RoomService = Depends(get_room_service)
) -> RoomOut:
    return service.get_by_id(room_id)


@router.post("/", response_model=RoomOut, status_code=201)
async def create_room(
        room: RoomIn,
        service: RoomService = Depends(get_room_service)
) -> RoomOut:
    return service.create(room)


@router.put("/{room_id}", response_model=RoomOut)
async def update_room(
        room_id: int,
        update: RoomUpdate,
        service: RoomService = Depends(get_room_service)
) -> RoomOut:
    return service.update(room_id, update)


@router.delete("/{room_id}", status_code=200)
async def delete_room(
        room_id: int,
        service: RoomService = Depends(get_room_service)
):
    service.delete(room_id)
    return {"message": "Room deleted successfully"}
