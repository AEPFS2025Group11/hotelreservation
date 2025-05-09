import logging

from fastapi import APIRouter, Depends

from app.auth.dependencies import admin_only
from app.services.booking_service import BookingService, get_booking_service
from app.services.models.booking_models import BookingOut, BookingIn, BookingUpdate

router = APIRouter(prefix="/api/bookings", tags=["bookings"])
logger = logging.getLogger(__name__)

@router.get("/", response_model=list[BookingOut], dependencies=[Depends(admin_only)])
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


@router.patch("/{booking_id}/cancel", response_model=BookingOut)
async def cancel_booking(
        booking_id: int,
        service: BookingService = Depends(get_booking_service)
):
    logger.info(f"PATCH /api/bookings/{booking_id}/cancel - Cancelling booking")
    return service.cancel_booking(booking_id)
