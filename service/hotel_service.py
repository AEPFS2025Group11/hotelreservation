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
from app.util.dynamic_pricing import calculate_dynamic_price

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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
        logger.info(f"Fetching hotels with filters: city='{city}', min_stars={min_stars}, "
                    f"capacity={capacity}, check_in={check_in}, check_out={check_out}")
        if check_in and check_out and check_in > check_out:
            logger.warning("Invalid date range: check_out < check_in")
            raise HTTPException(status_code=400, detail="Check out must be greater than check_in")

        hotels = self.hotel_repo.get_filtered(city, min_stars, capacity, check_in, check_out)
        logger.info(f"{len(hotels)} hotel(s) found")
        return [HotelOut.model_validate(h) for h in hotels]

    def get_by_id(self, hotel_id: int) -> HotelOut:
        logger.info(f"Fetching hotel by ID: {hotel_id}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            logger.warning(f"Hotel ID {hotel_id} not found")
            raise HTTPException(status_code=404, detail="Hotel not found")
        return HotelOut.model_validate(hotel)

    def create(self, hotel_data: HotelIn) -> HotelOut:
        logger.info(f"Creating new hotel: {hotel_data.name}")
        hotel = Hotel(
            name=hotel_data.name,
            stars=hotel_data.stars,
            address_id=hotel_data.address_id
        )
        created = self.hotel_repo.create(hotel)
        logger.info(f"Hotel created with ID {created.id}")
        return HotelOut.model_validate(created)

    def update(self, hotel_id: int, data: HotelUpdate) -> HotelOut:
        logger.info(f"Updating hotel ID {hotel_id}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            logger.warning(f"Hotel ID {hotel_id} not found for update")
            raise HTTPException(status_code=404, detail="Hotel not found")

        if data.name is not None:
            hotel.name = data.name
        if data.stars is not None:
            hotel.stars = data.stars

        updated = self.hotel_repo.update(hotel)
        logger.info(f"Hotel ID {hotel_id} updated successfully")
        return HotelOut.model_validate(updated)

    def delete(self, hotel_id: int) -> HotelOut:
        logger.info(f"Deleting hotel ID {hotel_id}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            logger.warning(f"Hotel ID {hotel_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Hotel not found")

        deleted = self.hotel_repo.delete(hotel_id)
        logger.info(f"Hotel ID {hotel_id} deleted")
        return HotelOut.model_validate(deleted)

    def get_rooms(self,
                  hotel_id: int,
                  capacity: Optional[int] = None,
                  check_in: Optional[date] = None,
                  check_out: Optional[date] = None
                  ) -> list[RoomOut]:
        logger.info(f"Fetching rooms for hotel ID {hotel_id} with capacity={capacity}, "
                    f"check_in={check_in}, check_out={check_out}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            logger.warning(f"Hotel ID {hotel_id} not found when fetching rooms")
            raise HTTPException(status_code=404, detail="Hotel not found")

        if check_in and check_out and check_in > check_out:
            logger.warning("Invalid date range for room search")
            raise HTTPException(status_code=400, detail="Check out must be greater than check_in")

        rooms = self.room_repo.get_by_hotel_id(hotel_id, capacity, check_in, check_out)
        logger.info(f"{len(rooms)} room(s) found for hotel ID {hotel_id}")
        room_dtos = [RoomOut.model_validate(r) for r in rooms]
        for room in room_dtos:
            room.dynamic_price_per_night = calculate_dynamic_price(room.price_per_night, check_in)
            if check_in and check_out:
                nights = (check_out - check_in).days
                room.total_price = room.dynamic_price_per_night * nights
        return room_dtos
