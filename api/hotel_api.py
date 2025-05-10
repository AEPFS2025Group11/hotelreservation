import logging
from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from app.auth.dependencies import admin_only
from app.services.hotel_service import HotelService, get_hotel_service
from app.services.models.hotel_models import HotelOut, HotelIn, HotelUpdate
from app.services.models.room_models import RoomOut

router = APIRouter(prefix="/api/hotels", tags=["hotels"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[HotelOut])
async def get_hotels(
        city: Optional[str] = None,
        min_stars: Optional[int] = None,
        capacity: Optional[int] = None,
        check_in: Optional[date] = None,
        check_out: Optional[date] = None,
        service: HotelService = Depends(get_hotel_service)
) -> list[HotelOut]:
    logger.info(
        f"GET /api/hotels - city={city}, min_stars={min_stars}, capacity={capacity}, check_in={check_in}, check_out={check_out}")
    return service.get_hotels(city, min_stars, capacity, check_in, check_out)


@router.get("/admin", response_model=list[HotelOut], dependencies=[Depends(admin_only)])
async def get_all_hotels(
        service: HotelService = Depends(get_hotel_service)
) -> list[HotelOut]:
    logger.info(
        f"GET /api/hotels/admin")
    return service.get_all_hotels()


@router.get("/{hotel_id}", response_model=HotelOut)
async def get_hotel(
        hotel_id: int,
        service: HotelService = Depends(get_hotel_service)
) -> HotelOut:
    logger.info(f"GET /api/hotels/{hotel_id} - Fetching hotel")
    hotel = service.get_by_id(hotel_id)
    if hotel is None:
        logger.warning(f"Hotel with ID {hotel_id} not found")
        raise HTTPException(status_code=404, detail="Hotel konnte nicht gefunden werden.")
    return hotel


@router.post("/", response_model=HotelOut, status_code=201)
async def create_hotel(
        hotel: HotelIn,
        service: HotelService = Depends(get_hotel_service)
) -> HotelOut:
    logger.info(f"POST /api/hotels - Creating hotel: {hotel.name}")
    return service.create(hotel)


@router.put("/{hotel_id}", response_model=HotelOut)
async def update_hotel(
        hotel_id: int,
        update: HotelUpdate,
        service: HotelService = Depends(get_hotel_service)
) -> HotelOut:
    logger.info(f"PUT /api/hotels/{hotel_id} - Updating hotel")
    return service.update(hotel_id, update)


@router.delete("/{hotel_id}", status_code=200, response_model=HotelOut)
async def delete_hotel(
        hotel_id: int,
        service: HotelService = Depends(get_hotel_service)
):
    logger.info(f"DELETE /api/hotels/{hotel_id} - Deleting hotel")

    return service.delete(hotel_id)


@router.get("/{hotel_id}/rooms", response_model=list[RoomOut])
def get_rooms_by_hotel(
        hotel_id: int,
        capacity: Optional[int] = None,
        check_in: Optional[date] = None,
        check_out: Optional[date] = None,
        service: HotelService = Depends(get_hotel_service)
):
    logger.info(f"GET /api/hotels/{hotel_id}/rooms - capacity={capacity}, check_in={check_in}, check_out={check_out}")
    return service.get_rooms(hotel_id, capacity, check_in, check_out)
