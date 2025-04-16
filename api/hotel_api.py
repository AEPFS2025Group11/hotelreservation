from datetime import date
from functools import lru_cache
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from app.repository.address_repository import AddressRepository
from app.repository.hotel_repository import HotelRepository
from app.repository.room_repository import RoomRepository
from app.service.hotel_service import HotelService
from app.service.models.hotel_models import HotelOut, HotelIn, HotelUpdate
from app.service.models.room_models import RoomOut

router = APIRouter(prefix="/api/hotels", tags=["hotels"])


@lru_cache()
def get_hotel_service() -> HotelService:
    room_repo = RoomRepository()
    hotel_repo = HotelRepository()
    address_repo = AddressRepository()
    return HotelService(
        room_repo=room_repo,
        hotel_repo=hotel_repo,
        address_repo=address_repo
    )


@router.get("/", response_model=list[HotelOut])
async def get_hotels(
        city: Optional[str] = None,
        min_stars: Optional[int] = None,
        capacity: Optional[int] = None,
        check_in: Optional[date] = None,
        check_out: Optional[date] = None,
        service: HotelService = Depends(get_hotel_service)
) -> list[HotelOut]:
    return service.get_hotels(city, min_stars, capacity, check_in, check_out)


@router.get("/{hotel_id}", response_model=HotelOut)
async def get_hotel(
        hotel_id: int,
        service: HotelService = Depends(get_hotel_service)
) -> HotelOut:
    hotel = service.get_by_id(hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.post("/", response_model=HotelOut, status_code=201)
async def create_hotel(
        hotel: HotelIn,
        service: HotelService = Depends(get_hotel_service)
) -> HotelOut:
    return service.create(hotel)


@router.put("/{hotel_id}", response_model=HotelOut)
async def update_hotel(
        hotel_id: int,
        update: HotelUpdate,
        service: HotelService = Depends(get_hotel_service)
) -> HotelOut:
    return service.update(hotel_id, update)


@router.delete("/{hotel_id}", status_code=200)
async def delete_hotel(
        hotel_id: int,
        service: HotelService = Depends(get_hotel_service)
):
    service.delete(hotel_id)
    return {"message": "Hotel deleted successfully"}


@router.get("/{hotel_id}/rooms", response_model=list[RoomOut])
def get_rooms_by_hotel(
        hotel_id: int,
        capacity: Optional[int] = None,
        check_in: Optional[date] = None,
        check_out: Optional[date] = None,
        service: HotelService = Depends(get_hotel_service)
):
    return service.get_rooms(hotel_id, capacity, check_in, check_out)
