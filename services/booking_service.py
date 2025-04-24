import logging
from datetime import datetime, timedelta, date

from fastapi import HTTPException

from app.repositories.booking_repository import BookingRepository
from app.entities.booking import Booking
from app.entities.user import User
from app.services.invoice_service import InvoiceService
from app.services.models.booking_models import BookingOut, BookingIn, BookingUpdate
from app.util.enums import InvoiceStatus

LOYALTY_POINTS = 10

AMOUNT_RECENT_BOOKINGS = 3

DAYS = 180

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BookingService:
    def __init__(
            self,
            booking_repo: BookingRepository,
            invoice_service: InvoiceService,
    ):
        self.booking_repo = booking_repo
        self.invoice_service = invoice_service

    def create(self, data: BookingIn) -> BookingOut:
        overlapping = self.booking_repo.get_overlapping_booking(
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out
        )

        if overlapping:
            raise HTTPException(status_code=400, detail="Room is already booked in that time range")

        booking = Booking(**data.model_dump())
        saved_booking = self.booking_repo.create(booking)
        self.invoice_service.create(saved_booking.id)
        self.award_loyalty_points(saved_booking)

        logger.info(f"Booking {saved_booking.id} created and invoice generated")
        return BookingOut.model_validate(saved_booking)

    def get_all(self) -> list[BookingOut]:
        logger.info("Fetching all bookings")
        bookings = self.booking_repo.get_all()
        logger.info(f"{len(bookings)} booking(s) found")
        return [BookingOut.model_validate(b) for b in bookings]

    def get_by_id(self, booking_id: int) -> BookingOut:
        logger.info(f"Fetching booking by ID: {booking_id}")
        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            logger.warning(f"Booking with ID {booking_id} not found")
            raise HTTPException(status_code=404, detail="Booking not found")
        return BookingOut.model_validate(booking)

    def update(self, booking_id: int, data: BookingUpdate) -> BookingOut:
        logger.info(f"Updating booking ID {booking_id} with data: {data.model_dump()}")
        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            logger.warning(f"Booking with ID {booking_id} not found for update")
            raise HTTPException(status_code=404, detail="Booking not found")

        if data.user_id is not None:
            booking.user_id = data.user_id
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
        self.award_loyalty_points(updated_booking)
        logger.info(f"Booking ID {booking_id} updated successfully")
        return BookingOut.model_validate(updated_booking)

    def delete(self, booking_id: int) -> BookingOut:
        logger.info(f"Deleting booking ID {booking_id}")
        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            logger.warning(f"Booking with ID {booking_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Booking not found")

        deleted = self.booking_repo.delete(booking_id)
        logger.info(f"Booking ID {booking_id} deleted successfully")
        return BookingOut.model_validate(deleted)

    def cancel_booking(self, booking_id: int) -> BookingOut:
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            logger.warning(f"Booking {booking_id} not found for cancellation")
            raise HTTPException(status_code=404, detail="Booking not found")

        if booking.is_cancelled:
            logger.info(f"Booking {booking_id} is already cancelled")
            raise HTTPException(status_code=400, detail="Booking is already cancelled")

        now = datetime.now().date()
        if now >= booking.check_in:
            logger.warning(f"Booking {booking_id} cannot be cancelled – check-in already started or in the past")
            raise HTTPException(status_code=400, detail="Cannot cancel booking that has already started or passed")

        if booking.check_in - timedelta(days=1) <= now:
            logger.warning(f"Booking {booking_id} cannot be cancelled – less than 24h before check-in")
            raise HTTPException(status_code=400, detail="Cancellation not allowed less than 24h before check-in")

        try:
            booking.is_cancelled = True
            booking.total_amount = 0
            updated_booking = self.booking_repo.update(booking)
            logger.info(f"Booking {booking_id} cancelled")

            if booking.invoice:
                invoice = self.invoice_service.invoice_repo.get_by_booking_id(booking.id)
                if not invoice:
                    logger.error(f"Invoice not found for booking {booking.id}")
                else:
                    invoice.total_amount = 0
                    invoice.status = InvoiceStatus.CANCELLED
                    self.invoice_service.invoice_repo.update(invoice)

            return BookingOut.model_validate(updated_booking)

        except Exception as e:
            self.booking_repo.db.rollback()
            logger.error(f"Error while cancelling booking {booking_id}: {e}")
            raise HTTPException(status_code=500, detail="Fehler beim Stornieren der Buchung.")

    def award_loyalty_points(self, booking: Booking):
        user_id = booking.user_id
        recent_bookings = (
            self.booking_repo.db.query(Booking)
            .filter(
                Booking.user_id == user_id,
                Booking.is_cancelled == False,
                Booking.check_out <= date.today(),
                Booking.check_out >= date.today() - timedelta(days=DAYS)
            )
            .count()
        )

        print(recent_bookings)

        if recent_bookings >= AMOUNT_RECENT_BOOKINGS:
            user = self.booking_repo.db.query(User).get(user_id)
            user.loyalty_points += LOYALTY_POINTS
            self.booking_repo.db.commit()
            logger.info(f"Awarded loyalty points to user ID {user_id}")

    def get_bookings_by_user_id(self, user_id: int) -> list[BookingOut]:
        logger.info(f"Fetching bookings for user ID {user_id}")
        bookings = self.booking_repo.get_by_user_id(user_id)

        if not bookings:
            logger.info(f"No bookings found for user ID {user_id}")
        else:
            logger.debug(f"{len(bookings)} booking(s) found for user ID {user_id}")

        return [BookingOut.model_validate(b) for b in bookings]
