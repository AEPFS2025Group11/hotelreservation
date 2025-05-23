import logging
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends

from app.auth.dependencies import admin_only
from app.services.models.room_models import RoomOut, RoomIn, RoomUpdate
from app.services.room_service import RoomService, get_room_service

router = APIRouter(prefix="/api/rooms", tags=["rooms"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[RoomOut])
async def get_rooms(
        city: Optional[str] = None,
        capacity: Optional[int] = None,
        check_in: Optional[date] = None,
        check_out: Optional[date] = None,
        service: RoomService = Depends(get_room_service)
) -> list[RoomOut]:
    logger.info(f"GET /api/rooms - city={city}, capacity={capacity}, check_in={check_in}, check_out={check_out}")
    return service.get_filtered(city, capacity, check_in, check_out)


@router.get("/admin", response_model=list[RoomOut], dependencies=[Depends(admin_only)])
async def get_rooms(
        service: RoomService = Depends(get_room_service)
) -> list[RoomOut]:
    logger.info(f"GET /api/rooms/admin")
    return service.get_all()


@router.get("/{room_id}", response_model=RoomOut)
async def get_room(
        room_id: int,
        check_in: Optional[date] = None,
        check_out: Optional[date] = None,
        service: RoomService = Depends(get_room_service)
) -> RoomOut:
    logger.info(f"GET /api/rooms/{room_id} - Fetching room by ID")
    return service.get_by_id(room_id, check_in, check_out)


@router.post("/", response_model=RoomOut, status_code=201)
async def create_room(
        room: RoomIn,
        service: RoomService = Depends(get_room_service)
) -> RoomOut:
    logger.info(f"POST /api/rooms - Creating room with number: {room.room_number}")
    return service.create(room)


@router.put("/{room_id}", response_model=RoomOut)
async def update_room(
        room_id: int,
        update: RoomUpdate,
        service: RoomService = Depends(get_room_service)
) -> RoomOut:
    logger.info(f"PUT /api/rooms/{room_id} - Updating room")
    return service.update(room_id, update)


@router.patch("/{room_id}/price", response_model=RoomOut)
async def update_price(room_id: int, price: float, service: RoomService = Depends(get_room_service)):
    return service.update_price(room_id, price)


@router.delete("/{room_id}", status_code=200, response_model=RoomOut)
async def delete_room(
        room_id: int,
        service: RoomService = Depends(get_room_service)
):
    logger.info(f"DELETE /api/rooms/{room_id} - Deleting room")

    return service.delete(room_id)
