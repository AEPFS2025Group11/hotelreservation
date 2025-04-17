from functools import lru_cache
import logging
from typing import Optional

from fastapi import APIRouter, Depends

from app.repository.booking_repository import BookingRepository
from app.repository.guest_repository import GuestRepository
from app.service.guest_service import GuestService
from app.service.models.booking_models import BookingOut
from app.service.models.guest_models import GuestOut, GuestIn, GuestUpdate

router = APIRouter(prefix="/api/guests", tags=["guests"])
logger = logging.getLogger(__name__)


@lru_cache()
def get_guest_service() -> GuestService:
    return GuestService(
        guest_repo=GuestRepository(),
        booking_repo=BookingRepository()
    )


@router.get("/", response_model=list[GuestOut])
async def get_guests(service: GuestService = Depends(get_guest_service)):
    logger.info("GET /api/guests - Fetching all guests")
    return service.get_all()


@router.get("/{guest_id}", response_model=GuestOut)
async def get_guest(guest_id: int, service: GuestService = Depends(get_guest_service)):
    logger.info(f"GET /api/guests/{guest_id} - Fetching guest by ID")
    return service.get_by_id(guest_id)


@router.post("/", response_model=GuestOut)
async def create_guest(guest: GuestIn, service: GuestService = Depends(get_guest_service)):
    logger.info("POST /api/guests - Creating new guest")
    return service.create(guest)


@router.put("/{guest_id}", response_model=GuestOut)
async def update_guest(guest_id: int, guest_update: GuestUpdate, service: GuestService = Depends(get_guest_service)):
    logger.info(f"PUT /api/guests/{guest_id} - Updating guest")
    return service.update(guest_id, guest_update)


@router.delete("/{guest_id}", response_model=GuestOut)
async def delete_guest(guest_id: int, service: GuestService = Depends(get_guest_service)):
    logger.info(f"DELETE /api/guests/{guest_id} - Deleting guest")
    return service.delete(guest_id)


@router.get("/{guest_id}/bookings", response_model=list[BookingOut])
async def get_bookings_by_guest_id(guest_id: int, upcoming: Optional[bool] = None,
                                   service: GuestService = Depends(get_guest_service)):
    logger.info(f"GET /api/guests/{guest_id}/bookings - Fetching guest bookings")
    return service.get_bookings_by_guest_id(guest_id, upcoming=upcoming)
