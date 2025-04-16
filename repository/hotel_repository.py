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


class HotelRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), Hotel)

    def get_by_address_id(self, address_id):
        return self.db.query(self.model).filter(self.model.address_id == address_id).first()

    def get_filtered(self, city: Optional[str], min_stars: Optional[int], capacity=None, check_in=None, check_out=None):
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

        return query.distinct().all()
