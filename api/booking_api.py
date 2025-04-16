from functools import lru_cache
import logging

from fastapi import APIRouter, Depends

from app.repository.booking_repository import BookingRepository
from app.service.booking_service import BookingService
from app.service.models.booking_models import BookingOut, BookingIn, BookingUpdate

router = APIRouter(prefix="/api/bookings", tags=["bookings"])
logger = logging.getLogger(__name__)


@lru_cache()
def get_booking_service() -> BookingService:
    return BookingService(booking_repo=BookingRepository())


@router.get("/", response_model=list[BookingOut])
async def get_bookings(service: BookingService = Depends(get_booking_service)):
    logger.info("GET /api/bookings - Fetching all bookings")
    return service.get_all()


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(booking_id: int, service: BookingService = Depends(get_booking_service)):
    logger.info(f"GET /api/bookings/{booking_id} - Fetching booking by ID")
    return service.get_by_id(booking_id)


@router.put("/{booking_id}", response_model=BookingOut)
async def update_booking(booking_id: int, booking_update: BookingUpdate,
                         service: BookingService = Depends(get_booking_service)):
    logger.info(f"PUT /api/bookings/{booking_id} - Updating booking")
    return service.update(booking_id, booking_update)


@router.delete("/{booking_id}", response_model=BookingOut)
async def delete_booking(booking_id: int, service: BookingService = Depends(get_booking_service)):
    logger.info(f"DELETE /api/bookings/{booking_id} - Deleting booking")
    return service.delete(booking_id)


@router.post("/", response_model=BookingOut)
async def create_booking(booking: BookingIn, service: BookingService = Depends(get_booking_service)):
    logger.info("POST /api/bookings - Creating new booking")
    return service.create(booking)
