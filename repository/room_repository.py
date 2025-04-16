import logging
import time
from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.entity.booking import Booking
from app.service.entity.facility import Facility
from app.service.entity.room import Room
from app.service.entity.room_type import RoomType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RoomRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self, city: Optional[str] = None,
                capacity: Optional[int] = None,
                check_in: Optional[date] = None,
                check_out: Optional[date] = None,
                hotel_id: Optional[int] = None) -> list[Room]:
        logger.info(f"Fetching all rooms with filters - city: {city}, capacity: {capacity}, "
                    f"check_in: {check_in}, check_out: {check_out}, hotel_id: {hotel_id}")
        start = time.perf_counter()

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
            logger.debug("Applying availability filter based on booking dates")
            subquery = select(Booking.room_id).where(
                Booking.check_in_date < check_out,
                Booking.check_out_date > check_in
            ).subquery()
            query = query.filter(~Room.room_id.in_(select(subquery.c.room_id)))

        result = query.all()
        duration = time.perf_counter() - start
        logger.info(f"Found {len(result)} room(s) in {duration:.3f}s")
        return result

    def get_by_id(self, room_id: int) -> Room:
        logger.info(f"Fetching room by ID: {room_id}")
        room = self.db.query(Room).options(
            joinedload(Room.type),
            joinedload(Room.facilities),
            joinedload(Room.hotel)
        ).filter(Room.room_id == room_id).first()
        if room:
            logger.debug(f"Room data: {room.__dict__}")
            logger.info(f"Room with ID {room_id} found")
        else:
            logger.warning(f"Room with ID {room_id} not found in database")
        return room

    def get_by_hotel_id(self, hotel_id: int, capacity: Optional[int] = None,
                        check_in: Optional[date] = None,
                        check_out: Optional[date] = None) -> list[Room]:
        logger.info(f"Fetching rooms for hotel ID {hotel_id} with capacity {capacity}, "
                    f"check_in: {check_in}, check_out: {check_out}")
        start = time.perf_counter()

        query = self.db.query(Room).join(Facility).options(joinedload(Room.type)) \
            .filter(Room.hotel_id == hotel_id)

        if capacity is not None:
            query = query.join(Room.type).filter(RoomType.max_guests >= capacity)
        if check_in and check_out:
            logger.debug("Applying booking date filter for room availability")
            subquery = select(Booking.room_id).where(
                Booking.check_in_date < check_out,
                Booking.check_out_date > check_in
            )
            query = query.filter(~Room.room_id.in_(subquery))

        rooms = query.all()
        duration = time.perf_counter() - start
        logger.info(f"Found {len(rooms)} room(s) for hotel ID {hotel_id} in {duration:.3f}s")
        return rooms

    def create(self, room_entity: Room) -> Room:
        logger.info(f"Creating new room with data: {room_entity}")
        try:
            self.db.add(room_entity)
            self.db.commit()
            self.db.refresh(room_entity)
            logger.info(f"Room created with ID {room_entity.room_id}")
            return room_entity
        except Exception as e:
            logger.error(f"Error creating room: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create room")

    def update(self, room_entity: Room) -> Room:
        logger.info(f"Updating room with ID {room_entity.room_id}")
        try:
            self.db.commit()
            self.db.refresh(room_entity)
            logger.info(f"Room with ID {room_entity.room_id} updated successfully")
            return room_entity
        except Exception as e:
            logger.error(f"Failed to update room with ID {room_entity.room_id}: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to update room")

    def delete(self, room_id: int):
        logger.info(f"Deleting room with ID {room_id}")
        room = self.db.query(Room).filter(Room.room_id == room_id).first()
        if room is None:
            logger.warning(f"Room with ID {room_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Room not found")
        try:
            self.db.delete(room)
            self.db.commit()
            logger.info(f"Room with ID {room_id} deleted successfully")
            return room
        except Exception as e:
            logger.error(f"Failed to delete room with ID {room_id}: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to delete room")
