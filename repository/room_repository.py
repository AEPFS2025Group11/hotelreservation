from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.repository.base_repository import BaseRepository
from app.service.entity.booking import Booking
from app.service.entity.hotel import Hotel
from app.service.entity.room import Room
from app.service.entity.room_type import RoomType


class RoomRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), Room)

    def get_all(self, city: Optional[str] = None, capacity: Optional[int] = None,
                check_in: Optional[date] = None, check_out: Optional[date] = None,
                hotel_id: Optional[int] = None) -> list[Room]:
        query = self.db.query(Room).join(Room.type).join(Room.hotel).options(
            joinedload(Room.type),
            joinedload(Room.hotel),
            joinedload(Room.facilities)
        )

        if hotel_id:
            query = query.filter(Room.hotel_id == hotel_id)
        if city:
            query = query.filter(Hotel.address.city == city)
        if capacity:
            query = query.filter(RoomType.max_guests == capacity)
        if check_in and check_out:
            subquery = select(Booking.room_id).where(
                Booking.check_in < check_out,
                Booking.check_out > check_in
            ).subquery()
            query = query.filter(~Room.id.in_(select(subquery.c.room_id)))
        return query.all()

    def get_by_hotel_id(self, hotel_id: int, capacity: Optional[int] = None,
                        check_in: Optional[date] = None, check_out: Optional[date] = None) -> list[Room]:
        query = self.db.query(Room).join(Room.facilities).options(
            joinedload(Room.type),
            joinedload(Room.facilities)
        ).filter(Room.hotel_id == hotel_id)
        if capacity:
            query = query.join(Room.type).filter(RoomType.max_guests >= capacity)
        if check_in and check_out:
            subquery = select(Booking.room_id).where(
                Booking.check_in < check_out,
                Booking.check_out > check_in
            )
            query = query.filter(~Room.id.in_(subquery))
        return query.all()
