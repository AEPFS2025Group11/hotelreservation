import logging
from datetime import date
from typing import Optional

from fastapi import HTTPException

from app.repository.address_repository import AddressRepository
from app.repository.hotel_repository import HotelRepository
from app.repository.room_repository import RoomRepository
from app.service.entity.hotel import Hotel
from app.service.models.hotel_models import HotelOut, HotelIn, HotelUpdate
from app.service.models.room_models import RoomOut

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def add_total_price(check_in, check_out, room_dtos):
    if check_in and check_out:
        nights = (check_out - check_in).days
        if nights <= 0:
            logger.warning("Attempted to calculate total price with non-positive nights")
            return
        for room in room_dtos:
            room.total_price = room.price_per_night * nights
        logger.info(f"Added total_price to {len(room_dtos)} room(s) for {nights} night(s)")


class HotelService:
    def __init__(
            self,
            room_repo: RoomRepository,
            hotel_repo: HotelRepository,
            address_repo: AddressRepository,
    ):
        self.room_repo = room_repo
        self.hotel_repo = hotel_repo
        self.address_repo = address_repo

    def get_hotels(self, city: Optional[str] = None,
                   min_stars: Optional[int] = None,
                   capacity: Optional[int] = None,
                   check_in: Optional[date] = None,
                   check_out: Optional[date] = None) -> list[HotelOut]:
        logger.info(f"Fetching hotels in city='{city}', min_stars={min_stars}, "
                    f"capacity={capacity}, check_in={check_in}, check_out={check_out}")
        if check_in and check_out and check_in > check_out:
            logger.warning("Invalid date range: check_out is before check_in")
            raise HTTPException(status_code=400, detail="Check out must be greater than check_in")
        hotels = self.hotel_repo.get_filtered(city, min_stars, capacity, check_in, check_out)
        logger.info(f"Found {len(hotels)} hotel(s) matching the criteria")
        return [HotelOut.model_validate(h) for h in hotels]

    def get_by_id(self, hotel_id: int) -> HotelOut:
        logger.info(f"Fetching hotel by ID: {hotel_id}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if hotel is None:
            logger.warning(f"Hotel with ID {hotel_id} not found")
            raise HTTPException(status_code=404, detail="Hotel not found")
        return HotelOut.model_validate(hotel)

    def create(self, hotel_data: HotelIn) -> HotelOut:
        logger.info(f"Creating hotel: {hotel_data.name}")
        hotel = Hotel(
            name=hotel_data.name,
            stars=hotel_data.stars,
            address_id=hotel_data.address_id
        )
        hotel = self.hotel_repo.create(hotel)
        return HotelOut.model_validate(hotel)

    def update(self, hotel_id: int, data: HotelUpdate) -> HotelOut:
        logger.info(f"Updating hotel ID {hotel_id}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if hotel is None:
            logger.warning(f"Hotel with ID {hotel_id} not found for update")
            raise HTTPException(status_code=404, detail="Hotel not found")

        if data.name is not None:
            hotel.name = data.name
        if data.stars is not None:
            hotel.stars = data.stars

        updated_hotel = self.hotel_repo.update(hotel)
        return HotelOut.model_validate(updated_hotel)

    def delete(self, hotel_id: int) -> HotelOut:
        logger.info(f"Deleting hotel ID {hotel_id}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if hotel is None:
            logger.warning(f"Hotel with ID {hotel_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Hotel not found")
        return HotelOut.model_validate(self.hotel_repo.delete(hotel_id))

    def get_rooms(
            self,
            hotel_id: int,
            capacity: Optional[int] = None,
            check_in: Optional[date] = None,
            check_out: Optional[date] = None
    ) -> list[RoomOut]:
        logger.info(f"Fetching rooms for hotel ID {hotel_id} with capacity={capacity}, "
                    f"check_in={check_in}, check_out={check_out}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if hotel is None:
            logger.warning(f"Hotel with ID {hotel_id} not found when fetching rooms")
            raise HTTPException(status_code=404, detail="Hotel not found")

        if check_in and check_out and check_in > check_out:
            logger.warning("Invalid date range for room fetch: check_out is before check_in")
            raise HTTPException(status_code=400, detail="Check out must be greater than check_in")

        rooms = self.room_repo.get_by_hotel_id(hotel_id, capacity, check_in, check_out)
        logger.info(f"Found {len(rooms)} room(s) for hotel ID {hotel_id}")
        room_dtos = [RoomOut.model_validate(r) for r in rooms]
        add_total_price(check_in, check_out, room_dtos)
        return room_dtos
