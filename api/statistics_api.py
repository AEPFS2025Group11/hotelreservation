from fastapi import APIRouter, Depends
from functools import lru_cache

from app.service.statistics_service import StatisticsService
from app.repository.statistics_repository import StatisticsRepository

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@lru_cache()
def get_statistics_service():
    return StatisticsService(StatisticsRepository())


@router.get("/occupancy-by-room-type")
def occupancy_by_room_type(service: StatisticsService = Depends(get_statistics_service)):
    return service.get_occupancy_by_room_type()
