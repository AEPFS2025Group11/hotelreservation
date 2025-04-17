import logging
from functools import lru_cache

from fastapi import APIRouter, Depends

from app.repository.room_type import RoomTypeRepository
from app.service.room_type_service import RoomTypeService
from app.service.models.room_type_models import RoomTypeIn, RoomTypeOut

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/room_types", tags=["room_types"])


@lru_cache()
def get_service() -> RoomTypeService:
    return RoomTypeService(RoomTypeRepository())


@router.get("/", response_model=list[RoomTypeOut])
async def get_all_room_types(service: RoomTypeService = Depends(get_service)):
    logger.info("GET /api/room_types - Fetching all room types")
    return service.get_all()


@router.get("/{type_id}", response_model=RoomTypeOut)
async def get_room_type_by_id(type_id: int, service: RoomTypeService = Depends(get_service)):
    logger.info(f"GET /api/room_types/{type_id} - Fetching room type by ID")
    return service.get_by_id(type_id)


@router.post("/", response_model=RoomTypeOut)
async def create_room_type(data: RoomTypeIn, service: RoomTypeService = Depends(get_service)):
    logger.info("POST /api/room_types - Creating new room type")
    return service.create(data)


@router.put("/{type_id}", response_model=RoomTypeOut)
async def update_room_type(type_id: int, data: RoomTypeIn, service: RoomTypeService = Depends(get_service)):
    logger.info(f"PUT /api/room_types/{type_id} - Updating room type")
    return service.update(type_id, data)


@router.delete("/{type_id}", response_model=RoomTypeOut)
async def delete_room_type(type_id: int, service: RoomTypeService = Depends(get_service)):
    logger.info(f"DELETE /api/room_types/{type_id} - Deleting room type")
    return service.delete(type_id)
