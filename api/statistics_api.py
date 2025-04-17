from functools import lru_cache

from fastapi import APIRouter, Depends

from app.repository.statistics_repository import StatisticsRepository
from app.service.statistics_service import StatisticsService

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@lru_cache()
def get_statistics_service() -> StatisticsService:
    return StatisticsService(StatisticsRepository())


@router.get("/occupancy-by-room-type")
def occupancy_by_room_type(service: StatisticsService = Depends(get_statistics_service)):
    return service.get_occupancy_by_room_type()


@router.get("/demographics")
async def get_demographics(service: StatisticsService = Depends(get_statistics_service)):
    return service.get_demographics()
