# app/service/facility_service.py
import logging
from fastapi import HTTPException

from app.repository.facility_repository import FacilityRepository
from app.service.models.facility_models import FacilityIn, FacilityOut, FacilityUpdate

logger = logging.getLogger(__name__)


class FacilityService:
    def __init__(self, repo: FacilityRepository):
        self.repo = repo

    def get_all(self) -> list[FacilityOut]:
        facilities = self.repo.get_all()
        return [FacilityOut.model_validate(f) for f in facilities]

    def get_by_id(self, id_: int) -> FacilityOut:
        facility = self.repo.get_by_id(id_)
        return FacilityOut.model_validate(facility)

    def create(self, data: FacilityIn) -> FacilityOut:
        logger.info(f"Creating facility: {data.facility_name}")
        entity = self.repo.model(**data.model_dump())
        return FacilityOut.model_validate(self.repo.create(entity))

    def update(self, id_: int, data: FacilityUpdate) -> FacilityOut:
        facility = self.repo.get_by_id(id_)
        if not facility:
            raise HTTPException(status_code=404, detail="Facility not found")
        if not data:
            logger.info(f"No update: {data.facility.name}")
        facility.facility_name = data.facility_name
        return FacilityOut.model_validate(self.repo.update(facility))

    def delete(self, id_: int) -> FacilityOut:
        return FacilityOut.model_validate(self.repo.delete(id_))
