import logging
from functools import lru_cache
from fastapi import APIRouter, Depends

from app.repositories.facility_repository import FacilityRepository
from app.services.facility_service import FacilityService
from app.services.models.facility_models import FacilityIn, FacilityOut, FacilityUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/facilities", tags=["facilities"])


@lru_cache()
def get_service() -> FacilityService:
    return FacilityService(FacilityRepository())


@router.get("/", response_model=list[FacilityOut])
async def get_facilities(service: FacilityService = Depends(get_service)):
    logger.info("GET /api/facilities - Fetching all facilities")
    return service.get_all()


@router.get("/{facility_id}", response_model=FacilityOut)
async def get_facility_by_id(facility_id: int, service: FacilityService = Depends(get_service)):
    logger.info(f"GET /api/facilities/{facility_id} - Fetching facility by ID")
    return service.get_by_id(facility_id)


@router.post("/", response_model=FacilityOut)
async def create_facility(data: FacilityIn, service: FacilityService = Depends(get_service)):
    logger.info("POST /api/facilities - Creating new facility")
    return service.create(data)


@router.put("/{facility_id}", response_model=FacilityOut)
async def update_facility(facility_id: int, data: FacilityUpdate, service: FacilityService = Depends(get_service)):
    logger.info(f"PUT /api/facilities/{facility_id} - Updating facility")
    return service.update(facility_id, data)


@router.delete("/{facility_id}", response_model=FacilityOut)
async def delete_facility(facility_id: int, service: FacilityService = Depends(get_service)):
    logger.info(f"DELETE /api/facilities/{facility_id} - Deleting facility")
    return service.delete(facility_id)
