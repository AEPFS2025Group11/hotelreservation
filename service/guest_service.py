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

    def create(self, data: GuestIn) -> GuestOut:
        guest = Guest(**data.model_dump())
        saved = self.guest_repo.create(guest)
        return GuestOut.model_validate(saved)

    def get_all(self) -> list[GuestOut]:
        return [GuestOut.model_validate(b) for b in self.guest_repo.get_all()]

    def get_by_id(self, guest_id):
        return GuestOut.model_validate(self.guest_repo.get_by_id(guest_id))

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
            guest.email = data.email
        if data.address_id is not None:
            guest.address_id = data.address_id
        updated_guest = self.guest_repo.update(guest)
        return GuestOut.model_validate(updated_guest)

    def delete(self, guest_id: int) -> GuestOut:
        logger.info(f"Deleting guest ID {guest_id}")
        guest = self.guest_repo.get_by_id(guest_id)
        if guest is None:
            logger.warning(f"Guest with ID {guest_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Guest not found")
        return GuestOut.model_validate(self.guest_repo.delete(guest_id))

    def get_bookings_by_guest_id(self, guest_id: int) -> list[BookingOut]:
        return [BookingOut.model_validate(b) for b in self.booking_repo.get_by_guest_id(guest_id)]
