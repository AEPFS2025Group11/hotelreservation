from fastapi import APIRouter

from app.service.models.room_models import RoomOut, RoomIn, RoomUpdate
from app.service.room_service import RoomService

router = APIRouter(prefix="/api/rooms", tags=["rooms"])
room_service = RoomService()


@router.get("/", response_model=list[RoomOut])
async def get_rooms() -> list[RoomOut]:
    return room_service.get_all()


@router.get("/{room_id}", response_model=RoomOut)
async def get_room(room_id: int) -> RoomOut:
    return room_service.get_by_id(room_id)


@router.post("/", response_model=RoomOut, status_code=201)
async def create_room(room: RoomIn) -> RoomOut:
    return room_service.create(room)


@router.put("/{room_id}", response_model=RoomOut)
async def update_room(room_id: int, update: RoomUpdate) -> RoomOut:
    print(update)
    updated_room = room_service.update(room_id, update)
    return updated_room


@router.delete("/{room_id}", status_code=200)
async def delete_room(room_id: int):
    room_service.delete(room_id)
    return {"message": "Room deleted successfully"}
