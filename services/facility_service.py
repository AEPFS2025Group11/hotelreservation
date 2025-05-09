import logging

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.facility_repository import FacilityRepository
from app.services.models.facility_models import FacilityIn, FacilityOut, FacilityUpdate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FacilityService:
    def __init__(self, db: Session):
        self.repo = FacilityRepository(db=db)

    def get_all(self) -> list[FacilityOut]:
        logger.info("Fetching all facilities")
        facilities = self.repo.get_all()
        return [FacilityOut.model_validate(f) for f in facilities]

    def get_by_id(self, id_: int) -> FacilityOut:
        logger.info(f"Fetching facility by ID: {id_}")
        facility = self.repo.get_by_id(id_)
        if not facility:
            logger.warning(f"Facility with ID {id_} not found")
            raise HTTPException(status_code=404, detail="Facility not found")
        return FacilityOut.model_validate(facility)

    def create(self, data: FacilityIn) -> FacilityOut:
        logger.info(f"Creating facility: {data.facility_name}")
        entity = self.repo.model(**data.model_dump())
        created = self.repo.create(entity)
        logger.info(f"Facility created with ID {created.id}")
        return FacilityOut.model_validate(created)

    def update(self, id_: int, data: FacilityUpdate) -> FacilityOut:
        logger.info(f"Updating facility ID {id_}")
        facility = self.repo.get_by_id(id_)
        if not facility:
            logger.warning(f"Facility ID {id_} not found for update")
            raise HTTPException(status_code=404, detail="Facility not found")

        if data.facility_name is not None:
            facility.facility_name = data.facility_name
        else:
            logger.info("No fields provided for update")

        updated = self.repo.update(facility)
        logger.info(f"Facility ID {id_} updated")
        return FacilityOut.model_validate(updated)

    def delete(self, id_: int) -> FacilityOut:
        logger.info(f"Deleting facility ID {id_}")
        deleted = self.repo.delete(id_)
        logger.info(f"Facility ID {id_} deleted")
        return FacilityOut.model_validate(deleted)


def get_facility_service(db: Session = Depends(get_db)) -> FacilityService:
    return FacilityService(db=db)
