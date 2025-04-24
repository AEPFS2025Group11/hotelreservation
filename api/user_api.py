import logging
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException

from app.repositories.booking_repository import BookingRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.user_repository import UserRepository
from app.services.booking_service import BookingService
from app.services.invoice_service import InvoiceService
from app.services.models.booking_models import BookingOut
from app.services.models.user_models import UserModel
from app.services.user_service import UserService

logger = logging.getLogger(__name__)


@lru_cache()
def get_user_service() -> UserService:
    logger.info("Initializing UserService via lru_cache")
    user_repo = UserRepository()
    return UserService(user_repo=user_repo)


@lru_cache()
def get_booking_service() -> BookingService:
    return BookingService(
        booking_repo=BookingRepository(),
        invoice_service=InvoiceService(
            invoice_repo=InvoiceRepository(),
            booking_repo=BookingRepository()
        )
    )


router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=list[UserModel])
def read_users(service: UserService = Depends(get_user_service)):
    logger.info("GET /users - Fetching all users")
    users = service.get_all_users()
    logger.debug(f"Fetched {len(users)} users")
    return users


@router.get("/{user_id}", response_model=UserModel)
def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    logger.info(f"GET /users/{user_id} - Fetching user by ID")
    user = service.get_user(user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.debug(f"User found: {user.email}")
    return user


@router.get("/{user_id}/bookings", response_model=list[BookingOut])
def get_bookings_by_user(user_id: int, service: BookingService = Depends(get_booking_service)):
    logger.info(f"GET /users/{user_id}/bookings - Fetching bookings by ID")
    bookings = service.get_bookings_by_user_id(user_id)
    if not bookings:
        logger.warning(f"No bookings found for user with ID {user_id}")
        raise HTTPException(status_code=404, detail="Bookings not found")
    logger.debug(f"{len(bookings)} bookings found for user ID {user_id}")
    return bookings


@router.put("/{user_id}", response_model=UserModel)
def update_user(user_id: int, user: UserModel, service: UserService = Depends(get_user_service)):
    logger.info(f"PUT /users/{user_id} - Updating user")
    updated_user = service.update_user(user_id, user)
    if not updated_user:
        logger.warning(f"Update failed: User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.debug(f"User {user_id} updated successfully")
    return updated_user


@router.delete("/{user_id}", response_model=UserModel)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    logger.info(f"DELETE /users/{user_id} - Deleting user")
    deleted = service.delete_user(user_id)
    if not deleted:
        logger.warning(f"Delete failed: User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.debug(f"User {user_id} deleted successfully")
    return deleted
