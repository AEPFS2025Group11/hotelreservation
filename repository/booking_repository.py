from datetime import date

from app.database.database import SessionLocal
from app.repository.base_repository import BaseRepository
from app.service.entity.booking import Booking


class BookingRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), Booking)

    def get_by_guest_id(self, guest_id: int) -> list[Booking]:
        booking = self.db.query(self.model).filter(self.model.guest_id == guest_id).all()
        return booking

    def get_overlapping_booking(self, room_id: int, check_in: date, check_out: date) -> bool:
        return self.db.query(Booking).filter(
            Booking.room_id == room_id,
            Booking.is_cancelled == False,
            Booking.check_in < check_out,
            Booking.check_out > check_in
        ).first() is not None
