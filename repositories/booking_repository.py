import logging
from datetime import date

from fastapi import HTTPException

from app.database.database import SessionLocal
from app.repositories.base_repository import BaseRepository
from app.entities.booking import Booking

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BookingRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), Booking)

    def get_by_user_id(self, user_id: int) -> list[Booking]:
        logger.info(f"Fetching bookings for user_id={user_id}")
        bookings = self.db.query(self.model).filter(self.model.user_id == user_id).all()
        logger.info(f"Found {len(bookings)} booking(s) for user_id={user_id}")
        return bookings

    def get_overlapping_booking(self, room_id: int, check_in: date, check_out: date) -> bool:
        logger.info(f"Checking for overlapping bookings: room_id={room_id}, "
                    f"check_in={check_in}, check_out={check_out}")
        overlapping = self.db.query(Booking).filter(
            Booking.room_id == room_id,
            Booking.is_cancelled == False,
            Booking.check_in < check_out,
            Booking.check_out > check_in
        ).first()
        if overlapping:
            logger.info(f"Overlapping booking found (booking_id={overlapping.id})")
        else:
            logger.info("No overlapping booking found")
        return overlapping is not None

    def cancel_booking(self, booking_id: int) -> Booking:
        logger.info(f"Cancelling booking ID {booking_id}")
        booking = self.get_by_id(booking_id)
        if not booking:
            logger.warning(f"Booking with ID {booking_id} not found for cancellation")
            raise HTTPException(status_code=404, detail="Booking not found")

        booking.is_cancelled = True
        self.db.commit()
        self.db.refresh(booking)
        logger.info(f"Booking ID {booking_id} marked as cancelled")
        return booking
