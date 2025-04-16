from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.service.hotel_service import HotelService
from app.service.models.hotel_models import HotelOut, HotelIn, HotelUpdate
from app.service.models.room_models import RoomOut

router = APIRouter(prefix="/api/hotels", tags=["hotels"])
hotel_service = HotelService()


@router.get("/", response_model=list[HotelOut])
async def get_hotels(city: Optional[str] = None,
                     min_stars: Optional[int] = None,
                     capacity: Optional[int] = None,
                     check_in: Optional[date] = None,
                     check_out: Optional[date] = None) -> list[HotelOut]:
    return hotel_service.get_hotels(city, min_stars, capacity, check_in, check_out)


@router.get("/{hotel_id}", response_model=HotelOut)
async def get_hotel(hotel_id: int) -> HotelOut:
    hotel = hotel_service.get_by_id(hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.post("/", response_model=HotelOut, status_code=201)
async def create_hotel(hotel: HotelIn) -> HotelOut:
    created_hotel = hotel_service.create(hotel)
    return created_hotel


@router.put("/{hotel_id}", response_model=HotelOut)
async def update_hotel(hotel_id: int, update: HotelUpdate) -> HotelOut:
    updated_hotel = hotel_service.update(hotel_id, update)
    return updated_hotel


@router.delete("/{hotel_id}", status_code=200)
async def delete_hotel(hotel_id: int):
    hotel_service.delete(hotel_id)
    return {"message": "Hotel deleted successfully"}


@router.get("/{hotel_id}/rooms", response_model=list[RoomOut])
def get_rooms_by_hotel(hotel_id: int,
                       capacity: Optional[int] = None,
                       check_in: Optional[date] = None,
                       check_out: Optional[date] = None):
    return hotel_service.get_rooms(hotel_id, capacity, check_in, check_out)
