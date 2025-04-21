from functools import lru_cache

from fastapi import APIRouter, Depends

from app.auth.dependencies import admin_only
from app.repository.booking_repository import BookingRepository
from app.repository.user_repository import UserRepository
from app.repository.statistics_repository import StatisticsRepository
from app.service.statistics_service import StatisticsService

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@lru_cache()
def get_statistics_service() -> StatisticsService:
    return StatisticsService(
        statistics_repo=StatisticsRepository(),
        user_repo=UserRepository(),
        booking_repo=BookingRepository()
    )


@router.get("/occupancy-by-room-type", dependencies=[Depends(admin_only)])
def occupancy_by_room_type(service: StatisticsService = Depends(get_statistics_service)):
    return service.get_occupancy_by_room_type()


@router.get("/demographics", dependencies=[Depends(admin_only)])
async def get_demographics(service: StatisticsService = Depends(get_statistics_service)):
    return service.get_demographics()
