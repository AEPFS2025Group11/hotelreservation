from sqlalchemy import func

from app.database.database import SessionLocal
from app.entities import Booking, Room
from app.entities import RoomType


class StatisticsRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_booking_count_by_room_type(self):
        return (
            self.db.query(RoomType.description, func.count(Booking.id))
            .join(Room, RoomType.id == Room.type_id)
            .join(Booking, Booking.room_id == Room.id, isouter=True)
            .filter((Booking.is_cancelled == False) | (Booking.id == None))
            .group_by(RoomType.description)
            .order_by(func.count(Booking.id).desc())
            .all()
        )
