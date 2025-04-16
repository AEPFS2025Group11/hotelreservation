from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import or_, and_, select
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.entity.booking import Booking
from app.service.entity.room_type import RoomType
from app.service.models.hotel_models import HotelIn, HotelUpdate
from app.service.entity.address import Address
from app.service.entity.hotel import Hotel
from app.service.entity.room import Room


class HotelRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self) -> list[Hotel]:
        return self.db.query(Hotel).options(joinedload(Hotel.address)).all()

    def get_by_id(self, hotel_id: int) -> Hotel:
        return self.db.query(Hotel).options(joinedload(Hotel.address)).filter(Hotel.hotel_id == hotel_id).first()

    def create(self, hotel_data: HotelIn) -> Hotel:
        address = self.db.query(Address).filter_by(address_id=hotel_data.address_id).first()

        if address is None:
            raise HTTPException(status_code=404, detail="Address not found")

        hotel = Hotel(name=hotel_data.name, stars=hotel_data.stars, address_id=address.address_id)
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def update(self, hotel_id: int, data: HotelUpdate) -> Hotel:
        hotel = self.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        if data.name is not None:
            hotel.name = data.name
        if data.stars is not None:
            hotel.stars = data.stars
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def delete(self, hotel_id: int) -> Hotel:
        hotel = self.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        self.db.delete(hotel)
        self.db.commit()
        return hotel

    def get_by_address_id(self, address_id) -> Hotel:
        return self.db.query(Hotel).filter(Hotel.address_id == address_id).first()

    def get_filtered(self, city: Optional[str], min_stars: Optional[int], capacity, check_in, check_out) -> list[Hotel]:
        query = self.db.query(Hotel).join(Hotel.rooms).join(Room.type).join(Hotel.address).options(
            joinedload(Hotel.rooms).joinedload(Room.type),
            joinedload(Hotel.address))

        if city:
            query = query.join(Hotel.address).filter(Address.city == city)

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
