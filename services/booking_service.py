import logging
from datetime import datetime, timedelta, date

from fastapi import HTTPException, Depends
from jose.jwt import utc_now
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.entities import Invoice
from app.entities.booking import Booking
from app.entities.user import User
from app.repositories.booking_repository import BookingRepository
from app.repositories.hotel_repository import HotelRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.user_repository import UserRepository
from app.services.models.booking_models import BookingOut, BookingIn, BookingUpdate
from app.util.booking_confirmation import send_booking_confirmation
from app.util.enums import InvoiceStatus

LOYALTY_POINTS = 10

AMOUNT_RECENT_BOOKINGS = 3

DAYS = 180

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BookingService:
    def __init__(
            self,
            db: Session):
        self.booking_repo = BookingRepository(db=db)
        self.invoice_repo = InvoiceRepository(db)
        self.user_repo = UserRepository(db=db)
        self.hotel_repo = HotelRepository(db=db)
        self.room_repo = RoomRepository(db=db)

    def create(self, booking: BookingIn) -> BookingOut:
        now = date.today()
        if booking.check_in <= now and booking.check_out <= now:
            raise HTTPException(status_code=500, detail="Die Zeitspanne darf nicht in der Vergangenheit liegen.")
        self._ensure_availability(booking)
        user = self._get_user(booking)
        room = self._get_room(booking)
        hotel = self._get_hotel(room.hotel_id)
        booking = Booking(**booking.model_dump())
        saved_booking = self.booking_repo.create(booking)
        if not saved_booking:
            raise HTTPException(status_code=500, detail="Booking konnte nicht erstellt werden.")
        self._generate_invoice(booking=saved_booking)
        self._award_loyalty_points(saved_booking)
        logger.info(f"Booking {saved_booking.id} created and invoice generated")
        try:
            send_booking_confirmation(
                to_email=user.email,
                guest_name=user.first_name,
                hotel_name=hotel.name,
                booking_id=saved_booking.id,
                check_in=saved_booking.check_in,
                check_out=saved_booking.check_out,
                room_type=room.type.description,
            )
        except Exception as e:
            logger.warning(f"Fehler beim Senden der Buchungsbestätigung: {e}")
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
            raise HTTPException(status_code=404, detail="Booking konnte nicht gefunden werden.")
        return BookingOut.model_validate(booking)

    def update(self, booking_id: int, data: BookingUpdate) -> BookingOut:
        logger.info(f"Updating booking ID {booking_id} with data: {data.model_dump()}")
        booking = self._get_booking(booking_id=booking_id)
        self._update_booking_fields(booking, data)
        if data.is_cancelled is not None or data.check_in is not None:
            self._update_invoice_on_cancellation_or_change(booking_id, data)
        updated_booking = self.booking_repo.update(booking)
        self._award_loyalty_points(updated_booking)
        logger.info(f"Booking ID {booking_id} updated successfully")
        return BookingOut.model_validate(updated_booking)

    def delete(self, booking_id: int) -> BookingOut:
        logger.info(f"Deleting booking ID {booking_id}")
        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            logger.warning(f"Booking with ID {booking_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Booking konnte nicht gefunden werden.")
        deleted = self.booking_repo.delete(booking_id)
        logger.info(f"Booking ID {booking_id} deleted successfully")
        return BookingOut.model_validate(deleted)

    def cancel_booking(self, booking_id: int) -> BookingOut:
        booking = self._get_booking(booking_id)
        self._check_if_cancelled(booking, booking_id)
        now = datetime.now().date()
        if now >= booking.check_in:
            logger.warning(f"Booking {booking_id} cannot be cancelled – check-in already started or in the past")
            raise HTTPException(status_code=400,
                                detail="Vergangene oder laufende Buchungen können nicht storniert werden.")
        if booking.check_in - timedelta(days=1) <= now:
            logger.warning(f"Booking {booking_id} cannot be cancelled – less than 24h before check-in")
            raise HTTPException(status_code=400,
                                detail="Stornierung innerhalb der letzten 24h vor dem Check-in sind nicht erlaubt.")
        try:
            booking.is_cancelled = True
            booking.total_amount = 0
            updated_booking = self.booking_repo.update(booking)
            logger.info(f"Booking {booking_id} cancelled")

            if booking.invoice:
                invoice = self.invoice_repo.get_by_booking_id(booking.id)
                if not invoice:
                    logger.error(f"Invoice not found for booking {booking.id}")
                else:
                    invoice.total_amount = 0
                    invoice.status = InvoiceStatus.CANCELLED
                    self.invoice_repo.update(invoice)

            return BookingOut.model_validate(updated_booking)

        except Exception as e:
            self.booking_repo.db.rollback()
            logger.error(f"Error while cancelling booking {booking_id}: {e}")
            raise HTTPException(status_code=500, detail="Fehler beim Stornieren der Buchung.")

    def get_bookings_by_user_id(self, user_id: int) -> list[BookingOut]:
        logger.info(f"Fetching bookings for user ID {user_id}")
        bookings = self.booking_repo.get_by_user_id(user_id)

        if not bookings:
            logger.info(f"No bookings found for user ID {user_id}")
        else:
            logger.debug(f"{len(bookings)} booking(s) found for user ID {user_id}")

        return [BookingOut.model_validate(b) for b in bookings]

    def _check_if_cancelled(self, booking, booking_id):
        if booking.is_cancelled:
            logger.info(f"Booking {booking_id} is already cancelled")
            raise HTTPException(status_code=400, detail="Booking ist bereits storniert.")

    def _award_loyalty_points(self, booking: Booking):
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

        if recent_bookings >= AMOUNT_RECENT_BOOKINGS:
            user = self.booking_repo.db.query(User).get(user_id)
            user.loyalty_points += LOYALTY_POINTS
            self.booking_repo.db.commit()
            logger.info(f"Awarded loyalty points to user ID {user_id}")

    def _generate_invoice(self, booking: Booking) -> Invoice:
        invoice = Invoice(
            booking_id=booking.id,
            issue_date=date.today(),
            total_amount=booking.total_amount
        )
        saved_invoice = self.invoice_repo.create(invoice)
        if not saved_invoice:
            raise HTTPException(status_code=500, detail="Invoice konnte nicht erstellt werden.")
        return saved_invoice

    def _ensure_availability(self, data):
        overlapping = self.booking_repo.get_overlapping_booking(
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out
        )
        if overlapping:
            raise HTTPException(status_code=400, detail="Zimmer ist während dieser Zeitspanne bereits gebucht.")

    def _get_booking(self, booking_id):
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            logger.warning(f"Booking {booking_id} not found for cancellation")
            raise HTTPException(status_code=404, detail="Booking konnte nicht gefunden werden.")
        return booking

    def _get_room(self, data):
        room = self.room_repo.get_by_id(data.room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Zimmer konnte nicht gefunden werden.")
        return room

    def _get_hotel(self, hotel_id):
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel konnte nicht gefunden werden.")
        return hotel

    def _get_user(self, data):
        user = self.user_repo.get_by_id(data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Benutzer konnte nicht gefunden werden.")
        return user

    def _update_invoice_on_cancellation_or_change(self, booking_id: int, data: BookingUpdate):
        invoice = self.invoice_repo.get_by_booking_id(booking_id=booking_id)
        if not invoice:
            raise ValueError(f"Keine Rechnung für Buchung mit ID {booking_id} gefunden.")

        if data.is_cancelled:
            invoice.status = InvoiceStatus.CANCELLED
            invoice.total_amount = 0
        elif data.check_in:
            if data.check_in > date.today():
                invoice.status = InvoiceStatus.PENDING
            else:
                invoice.status = InvoiceStatus.PAID
            if data.total_amount is not None:
                invoice.total_amount = data.total_amount
        self.invoice_repo.update(invoice)

    def _update_booking_fields(self, booking: Booking, data: BookingUpdate):
        if data.room_id is not None:
            booking.room_id = data.room_id
        if data.check_in is not None:
            booking.check_in = data.check_in
        if data.check_out is not None:
            booking.check_out = data.check_out
        if data.total_amount is not None:
            booking.total_amount = data.total_amount
        if data.is_cancelled is not None:
            booking.is_cancelled = data.is_cancelled


def get_booking_service(db: Session = Depends(get_db)) -> BookingService:
    return BookingService(db=db)
