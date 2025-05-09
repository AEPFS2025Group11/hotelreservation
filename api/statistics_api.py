from fastapi import APIRouter, Depends

from app.auth.dependencies import admin_only
from app.services.statistics_service import StatisticsService, get_statistics_service

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@router.get("/occupancy-by-room-type", dependencies=[Depends(admin_only)])
def occupancy_by_room_type(service: StatisticsService = Depends(get_statistics_service)):
    return service.get_occupancy_by_room_type()


@router.get("/demographics", dependencies=[Depends(admin_only)])
async def get_demographics(service: StatisticsService = Depends(get_statistics_service)):
    return service.get_demographics()
