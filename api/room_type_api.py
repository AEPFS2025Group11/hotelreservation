# app/api/room_type_api.py
from functools import lru_cache
from fastapi import APIRouter, Depends

from app.repository.room_type import RoomTypeRepository
from app.service.room_type_service import RoomTypeService
from app.service.models.room_type_models import RoomTypeIn, RoomTypeOut

router = APIRouter(prefix="/api/room_types", tags=["room_types"])


@lru_cache()
def get_service() -> RoomTypeService:
    return RoomTypeService(RoomTypeRepository())


@router.get("/", response_model=list[RoomTypeOut])
async def get_all(service: RoomTypeService = Depends(get_service)):
    return service.get_all()


@router.get("/{type_id}", response_model=RoomTypeOut)
async def get_by_id(type_id: int, service: RoomTypeService = Depends(get_service)):
    return service.get_by_id(type_id)


@router.post("/", response_model=RoomTypeOut)
async def create(data: RoomTypeIn, service: RoomTypeService = Depends(get_service)):
    return service.create(data)


@router.put("/{type_id}", response_model=RoomTypeOut)
async def update(type_id: int, data: RoomTypeIn, service: RoomTypeService = Depends(get_service)):
    return service.update(type_id, data)


@router.delete("/{type_id}", response_model=RoomTypeOut)
async def delete(type_id: int, service: RoomTypeService = Depends(get_service)):
    return service.delete(type_id)
