import logging
import re

from email_validator import validate_email, EmailSyntaxError, EmailUndeliverableError
from fastapi import HTTPException

from app.repository.booking_repository import BookingRepository
from app.repository.guest_repository import GuestRepository
from app.service.entity import Guest
from app.service.models.booking_models import BookingOut
from app.service.models.guest_models import GuestIn, GuestOut, GuestUpdate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def is_valid_phone(phone: str) -> bool:
    return re.match(r"^\+?[0-9\s\-()]{7,20}$", phone) is not None

class GuestService:
    def __init__(
            self,
            guest_repo: GuestRepository,
            booking_repo: BookingRepository,
    ):
        self.guest_repo = guest_repo
        self.booking_repo = booking_repo

    def create(self, data: GuestIn) -> GuestOut:
        logger.info(f"Creating new guest: {data.first_name} {data.last_name}")
        if data.phone_number is not None:
            if not is_valid_phone(data.phone_number):
                raise HTTPException(status_code=400, detail="Invalid phone number format")
            data.phone_number = data.phone_number
        try:
            validate_email(data.email)
        except (EmailSyntaxError, EmailUndeliverableError) as e:
            raise HTTPException(status_code=400, detail=str(e))
        guest = Guest(**data.model_dump())
        saved = self.guest_repo.create(guest)
        logger.info(f"Guest created with ID {saved.id}")
        return GuestOut.model_validate(saved)

    def get_all(self) -> list[GuestOut]:
        logger.info("Fetching all guests")
        guests = self.guest_repo.get_all()
        logger.info(f"Found {len(guests)} guest(s)")
        return [GuestOut.model_validate(g) for g in guests]

    def get_by_id(self, guest_id):
        logger.info(f"Fetching guest by ID: {guest_id}")
        guest = self.guest_repo.get_by_id(guest_id)
        if guest is None:
            logger.warning(f"Guest with ID {guest_id} not found")
            raise HTTPException(status_code=404, detail="Guest not found")
        return GuestOut.model_validate(guest)

    def update(self, guest_id: int, data: GuestUpdate) -> GuestOut:
        logger.info(f"Updating guest ID {guest_id}")
        guest = self.guest_repo.get_by_id(guest_id)
        if guest is None:
            logger.warning(f"Guest with ID {guest_id} not found for update")
            raise HTTPException(status_code=404, detail="Guest not found")

        if data.first_name is not None:
            guest.first_name = data.first_name
        if data.last_name is not None:
            guest.last_name = data.last_name
        if data.email is not None:
            try:
                validate_email(data.email)
            except (EmailSyntaxError, EmailUndeliverableError) as e:
                raise HTTPException(status_code=400, detail=str(e))
            guest.email = data.email
        if data.phone_number is not None:
            if not is_valid_phone(data.phone_number):
                raise HTTPException(status_code=400, detail="Invalid phone number format")
            guest.phone_number = data.phone_number
        if data.address_id is not None:
            guest.address_id = data.address_id

        updated_guest = self.guest_repo.update(guest)
        logger.info(f"Guest with ID {guest_id} updated successfully")
        return GuestOut.model_validate(updated_guest)

    def delete(self, guest_id: int) -> GuestOut:
        logger.info(f"Deleting guest ID {guest_id}")
        guest = self.guest_repo.get_by_id(guest_id)
        if guest is None:
            logger.warning(f"Guest with ID {guest_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Guest not found")
        deleted = self.guest_repo.delete(guest_id)
        logger.info(f"Guest with ID {guest_id} deleted")
        return GuestOut.model_validate(deleted)

    def get_bookings_by_guest_id(self, guest_id: int) -> list[BookingOut]:
        logger.info(f"Fetching bookings for guest ID {guest_id}")
        bookings = self.booking_repo.get_by_guest_id(guest_id)
        logger.info(f"Found {len(bookings)} booking(s) for guest ID {guest_id}")
        return [BookingOut.model_validate(b) for b in bookings]
