from functools import lru_cache
from fastapi import APIRouter, Depends

from app.repository.facility_repository import FacilityRepository
from app.service.facility_service import FacilityService
from app.service.models.facility_models import FacilityIn, FacilityOut, FacilityUpdate

router = APIRouter(prefix="/api/facilities", tags=["facilities"])


@lru_cache()
def get_service() -> FacilityService:
    return FacilityService(FacilityRepository())


@router.get("/", response_model=list[FacilityOut])
async def get_all(service: FacilityService = Depends(get_service)):
    return service.get_all()


@router.get("/{facility_id}", response_model=FacilityOut)
async def get_by_id(facility_id: int, service: FacilityService = Depends(get_service)):
    return service.get_by_id(facility_id)


@router.post("/", response_model=FacilityOut)
async def create(data: FacilityIn, service: FacilityService = Depends(get_service)):
    return service.create(data)


@router.put("/{facility_id}", response_model=FacilityOut)
async def update(facility_id: int, data: FacilityUpdate, service: FacilityService = Depends(get_service)):
    return service.update(facility_id, data)


@router.delete("/{facility_id}", response_model=FacilityOut)
async def delete(facility_id: int, service: FacilityService = Depends(get_service)):
    return service.delete(facility_id)
