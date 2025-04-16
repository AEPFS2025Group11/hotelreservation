import logging
from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.repository.base_repository import BaseRepository
from app.service.entity.hotel import Hotel
from app.service.entity.room import Room
from app.service.entity.room_type import RoomType
from app.service.entity.address import Address
from app.service.entity.booking import Booking

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HotelRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), Hotel)

    def get_filtered(
            self,
            city: Optional[str] = None,
            min_stars: Optional[int] = None,
            capacity: Optional[int] = None,
            check_in: Optional[date] = None,
            check_out: Optional[date] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None
    ) -> list[Hotel]:
        logger.info(f"Filtering hotels with parameters: city='{city}', min_stars={min_stars}, "
                    f"capacity={capacity}, check_in={check_in}, check_out={check_out}, "
                    f"limit={limit}, offset={offset}")

        query = self.db.query(Hotel).join(Hotel.rooms).join(Room.type).join(Hotel.address).options(
            joinedload(Hotel.rooms).joinedload(Room.type),
            joinedload(Hotel.address)
        )

        if city:
            logger.debug(f"Filtering by city: {city}")
            query = query.filter(Address.city == city)

        if min_stars is not None:
            logger.debug(f"Filtering by min_stars >= {min_stars}")
            query = query.filter(Hotel.stars >= min_stars)

        if capacity is not None:
            logger.debug(f"Filtering by room capacity >= {capacity}")
            query = query.filter(RoomType.max_guests >= capacity)

        if check_in and check_out:
            logger.debug("Filtering by availability (excluding overlapping bookings)")
            subquery = select(Booking.room_id).where(
                Booking.check_in < check_out,
                Booking.check_out > check_in
            )
            query = query.filter(~Room.id.in_(subquery))

        query = query.distinct()

        if offset is not None:
            logger.debug(f"Applying offset: {offset}")
            query = query.offset(offset)

        if limit is not None:
            logger.debug(f"Applying limit: {limit}")
            query = query.limit(limit)

        result = query.all()
        logger.info(f"Returned {len(result)} hotel(s)")
        return result
