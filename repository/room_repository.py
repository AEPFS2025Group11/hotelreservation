from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.entity.booking import Booking
from app.service.entity.facility import Facility
from app.service.entity.hotel import Hotel
from app.service.entity.room import Room
from app.service.entity.room_type import RoomType


class RoomRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self, city: Optional[str] = None,
                capacity: Optional[int] = None,
                check_in: Optional[date] = None,
                check_out: Optional[date] = None,
                hotel_id: Optional[int] = None) -> list[Room]:
        query = self.db.query(Room).join(Room.type).join(Room.hotel).options(
            joinedload(Room.type),
            joinedload(Room.hotel),
            joinedload(Room.facilities)
        )
        if hotel_id:
            query = query.filter(Room.hotel_id == hotel_id)
        if city:
            query = query.filter(Room.hotel.city == city)
        if capacity:
            query = query.filter(Room.type.max_guests == capacity)
        if check_in and check_out:
            subquery = select(Booking.room_id).where(
                Booking.check_in_date < check_out,
                Booking.check_out_date > check_in
            ).subquery()

            query = query.filter(~Room.room_id.in_(select(subquery.c.room_id)))
        return query.all()

    def get_by_id(self, room_id: int) -> Room:
        return self.db.query(Room).filter(Room.room_id == room_id).join(RoomType).join(Facility).join(Hotel).first()

    def get_by_hotel_id(self, hotel_id: int, capacity: int, check_in, check_out) -> list[Room]:
        query = self.db.query(Room).join(Facility).options(joinedload(Room.type)).filter(Room.hotel_id == hotel_id)
        if capacity is not None:
            query = query.join(Room.type).filter(RoomType.max_guests >= capacity)
        if check_in and check_out:
            subquery = select(Booking.room_id).where(
                Booking.check_in_date < check_out,
                Booking.check_out_date > check_in
            )
            query = query.filter(~Room.room_id.in_(subquery))
        return query.all()

    def create(self, room_entity: Room) -> Room:
        self.db.add(room_entity)
        self.db.commit()
        self.db.refresh(room_entity)
        return room_entity

    def update(self, room_entity: Room) -> Room:
        self.db.commit()
        self.db.refresh(room_entity)
        return room_entity

    def delete(self, room_id: int):
        room = self.db.query(Room).filter(Room.room_id == room_id).first()
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        self.db.delete(room)
        self.db.commit()
        return room
