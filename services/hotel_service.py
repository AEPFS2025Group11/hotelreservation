import logging
from datetime import date
from typing import Optional

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.address_repository import AddressRepository
from app.repositories.hotel_repository import HotelRepository
from app.repositories.room_repository import RoomRepository
from app.entities.hotel import Hotel
from app.services.models.hotel_models import HotelOut, HotelIn, HotelUpdate
from app.services.models.room_models import RoomOut
from app.util.dynamic_pricing import calculate_dynamic_price

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HotelService:
    def __init__(
            self,
            db: Session
    ):
        self.room_repo = RoomRepository(db=db)
        self.hotel_repo = HotelRepository(db=db)
        self.address_repo = AddressRepository(db=db)

    def get_hotels(self, city: Optional[str] = None,
                   min_stars: Optional[int] = None,
                   capacity: Optional[int] = None,
                   check_in: Optional[date] = None,
                   check_out: Optional[date] = None) -> list[HotelOut]:
        logger.info(f"Fetching hotels with filters: city='{city}', min_stars={min_stars}, "
                    f"capacity={capacity}, check_in={check_in}, check_out={check_out}")
        if check_in and check_out and check_in > check_out:
            logger.warning("Invalid date range: check_out < check_in")
            raise HTTPException(status_code=400, detail="Check-Out muss nach dem Check-In liegen")

        hotels = self.hotel_repo.get_filtered(city, min_stars, capacity, check_in, check_out)
        logger.info(f"{len(hotels)} hotel(s) found")
        return [HotelOut.model_validate(h) for h in hotels]

    def get_by_id(self, hotel_id: int) -> HotelOut:
        logger.info(f"Fetching hotel by ID: {hotel_id}")
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            logger.warning(f"Hotel ID {hotel_id} not found")
            raise HTTPException(status_code=404, detail="Hotel konnte nicht gefunden werden.")
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
            raise HTTPException(status_code=404, detail="Hotel konnte nicht gefunden werden.")

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
            raise HTTPException(status_code=404, detail="Hotel konnte nicht gefunden werden.")

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
            raise HTTPException(status_code=404, detail="Hotel konnte nicht gefunden werden.")

        if check_in and check_out and check_in > check_out:
            logger.warning("Invalid date range for room search")
            raise HTTPException(status_code=400, detail="Check-Out muss nach dem Check-In liegen.")

        rooms = self.room_repo.get_by_hotel_id(hotel_id, capacity, check_in, check_out)
        logger.info(f"{len(rooms)} room(s) found for hotel ID {hotel_id}")
        room_dtos = [RoomOut.model_validate(r) for r in rooms]
        for room in room_dtos:
            room.dynamic_price_per_night = calculate_dynamic_price(room.price_per_night, check_in)
            if check_in and check_out:
                nights = (check_out - check_in).days
                room.total_price = room.dynamic_price_per_night * nights
        return room_dtos

    def get_all_hotels(self):
        return self.hotel_repo.get_all()


def get_hotel_service(db: Session = Depends(get_db)) -> HotelService:
    return HotelService(db=db)
