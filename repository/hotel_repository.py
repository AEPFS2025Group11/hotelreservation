import logging
from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.entity.booking import Booking
from app.service.entity.room_type import RoomType
from app.service.models.hotel_models import HotelIn, HotelUpdate
from app.service.entity.address import Address
from app.service.entity.hotel import Hotel
from app.service.entity.room import Room

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HotelRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self) -> list[Hotel]:
        logger.info("Fetching all hotels")
        return self.db.query(Hotel).options(joinedload(Hotel.address)).all()

    def get_by_id(self, hotel_id: int) -> Optional[Hotel]:
        logger.info(f"Fetching hotel by ID: {hotel_id}")
        hotel = self.db.query(Hotel).options(joinedload(Hotel.address)).filter(Hotel.hotel_id == hotel_id).first()
        if hotel:
            logger.debug(f"Hotel found: {hotel}")
        else:
            logger.warning(f"Hotel with ID {hotel_id} not found")
        return hotel

    def create(self, hotel_data: HotelIn) -> Hotel:
        logger.info(f"Creating hotel with data: {hotel_data}")
        address = self.db.query(Address).filter_by(address_id=hotel_data.address_id).first()

        if address is None:
            logger.warning(f"Address with ID {hotel_data.address_id} not found")
            raise HTTPException(status_code=404, detail="Address not found")

        hotel = Hotel(name=hotel_data.name, stars=hotel_data.stars, address_id=address.address_id)
        try:
            self.db.add(hotel)
            self.db.commit()
            self.db.refresh(hotel)
            logger.info(f"Hotel created with ID {hotel.hotel_id}")
            return hotel
        except Exception as e:
            logger.error(f"Failed to create hotel: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Could not create hotel")

    def update(self, hotel_id: int, data: HotelUpdate) -> Hotel:
        logger.info(f"Updating hotel with ID {hotel_id}")
        hotel = self.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")

        if data.name is not None:
            hotel.name = data.name
        if data.stars is not None:
            hotel.stars = data.stars

        try:
            self.db.commit()
            self.db.refresh(hotel)
            logger.info(f"Hotel with ID {hotel_id} updated successfully")
            return hotel
        except Exception as e:
            logger.error(f"Failed to update hotel ID {hotel_id}: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Could not update hotel")

    def delete(self, hotel_id: int) -> Hotel:
        logger.info(f"Deleting hotel with ID {hotel_id}")
        hotel = self.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")

        try:
            self.db.delete(hotel)
            self.db.commit()
            logger.info(f"Hotel with ID {hotel_id} deleted successfully")
            return hotel
        except Exception as e:
            logger.error(f"Failed to delete hotel ID {hotel_id}: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Could not delete hotel")

    def get_by_address_id(self, address_id: int) -> Optional[Hotel]:
        logger.info(f"Fetching hotel by address ID: {address_id}")
        return self.db.query(Hotel).filter(Hotel.address_id == address_id).first()

    def get_filtered(self,
                     city: Optional[str],
                     min_stars: Optional[int],
                     capacity: Optional[int],
                     check_in: Optional[date],
                     check_out: Optional[date]) -> list[Hotel]:
        logger.info(f"Filtering hotels with: city={city}, min_stars={min_stars}, "
                    f"capacity={capacity}, check_in={check_in}, check_out={check_out}")
        query = self.db.query(Hotel).join(Hotel.rooms).join(Room.type).join(Hotel.address).options(
            joinedload(Hotel.rooms).joinedload(Room.type),
            joinedload(Hotel.address)
        )

        if city:
            query = query.filter(Address.city == city)

        if min_stars:
            query = query.filter(Hotel.stars >= min_stars)

        if capacity:
            query = query.filter(RoomType.max_guests >= capacity)

        if check_in and check_out:
            subquery = select(Booking.room_id).where(
                Booking.check_in_date < check_out,
                Booking.check_out_date > check_in
            )
            query = query.filter(~Room.room_id.in_(subquery))

        result = query.distinct().all()
        logger.info(f"Found {len(result)} hotel(s) matching filters")
        return result
