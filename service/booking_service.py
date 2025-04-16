import logging

from fastapi import HTTPException

from app.repository.booking_repository import BookingRepository
from app.service.entity.booking import Booking
from app.service.models.booking_models import BookingOut, BookingIn, BookingUpdate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BookingService:
    def __init__(
            self,
            booking_repo: BookingRepository,
    ):
        self.booking_repo = booking_repo

    def create(self, data: BookingIn) -> BookingOut:
        overlapping = self.booking_repo.get_overlapping_booking(
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out
        )

        if overlapping:
            raise HTTPException(status_code=400, detail="Room is already booked in that time range")

        booking = Booking(**data.model_dump())
        saved = self.booking_repo.create(booking)
        return BookingOut.model_validate(saved)

    def get_all(self) -> list[BookingOut]:
        return [BookingOut.model_validate(b) for b in self.booking_repo.get_all()]

    def get_by_id(self, booking_id):
        return BookingOut.model_validate(self.booking_repo.get_by_id(booking_id))

    def update(self, booking_id: int, data: BookingUpdate) -> BookingOut:
        logger.info(f"Updating booking ID {booking_id}")
        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            logger.warning(f"Booking with ID {booking_id} not found for update")
            raise HTTPException(status_code=404, detail="Booking not found")

        if data.guest_id is not None:
            booking.guest_id = data.guest_id
        if data.room_id is not None:
            booking.room_id = data.room_id
        if data.check_in is not None:
            booking.check_in = data.check_in
        if data.check_out is not None:
            booking.check_out = data.check_out
        if data.is_cancelled is not None:
            booking.is_cancelled = data.is_cancelled
        if data.total_amount is not None:
            booking.total_amount = data.total_amount

        updated_booking = self.booking_repo.update(booking)
        return BookingOut.model_validate(updated_booking)

    def delete(self, booking_id: int) -> BookingOut:
        logger.info(f"Deleting booking ID {booking_id}")
        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            logger.warning(f"Booking with ID {booking_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Booking not found")
        return BookingOut.model_validate(self.booking_repo.delete(booking_id))
