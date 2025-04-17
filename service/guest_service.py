import logging

from fastapi import HTTPException

from app.repository.booking_repository import BookingRepository
from app.repository.guest_repository import GuestRepository
from app.service.entity import Guest
from app.service.models.booking_models import BookingOut
from app.service.models.guest_models import GuestIn, GuestOut, GuestUpdate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GuestService:
    def __init__(
            self,
            guest_repo: GuestRepository,
            booking_repo: BookingRepository,
    ):
        self.guest_repo = guest_repo
        self.booking_repo = booking_repo

    def create(self, guest_in: GuestIn) -> GuestOut:
        logger.info(f"Creating new guest: {guest_in.first_name} {guest_in.last_name}")
        guest = Guest(**guest_in.model_dump())
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

    def update(self, guest_id: int, guest_update: GuestUpdate) -> GuestOut:
        logger.info(f"Updating guest ID {guest_id}")
        guest = self.guest_repo.get_by_id(guest_id)
        if guest is None:
            logger.warning(f"Guest with ID {guest_id} not found for update")
            raise HTTPException(status_code=404, detail="Guest not found")

        for field, value in guest_update.model_dump(exclude_unset=True).items():
            setattr(guest, field, value)

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
