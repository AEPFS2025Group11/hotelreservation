import logging

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.room_type_repository import RoomTypeRepository
from app.services.models.room_type_models import RoomTypeIn, RoomTypeOut

logger = logging.getLogger(__name__)


class RoomTypeService:
    def __init__(self, db: Session):
        self.repo = RoomTypeRepository(db)

    def get_all(self) -> list[RoomTypeOut]:
        logger.info("Fetching all room types")
        room_types = self.repo.get_all()
        return [RoomTypeOut.model_validate(r) for r in room_types]

    def get_by_id(self, id_: int) -> RoomTypeOut:
        logger.info(f"Fetching room type with ID: {id_}")
        rt = self.repo.get_by_id(id_)
        if not rt:
            logger.warning(f"Room type with ID {id_} not found")
            raise HTTPException(status_code=404, detail="Room type not found")
        return RoomTypeOut.model_validate(rt)

    def create(self, data: RoomTypeIn) -> RoomTypeOut:
        logger.info(f"Creating room type: {data.description}")
        entity = self.repo.model(**data.model_dump())
        created = self.repo.create(entity)
        logger.info(f"Room type created with ID {created.id}")
        return RoomTypeOut.model_validate(created)

    def update(self, id_: int, data: RoomTypeIn) -> RoomTypeOut:
        logger.info(f"Updating room type ID {id_}")
        entity = self.repo.get_by_id(id_)
        if not entity:
            logger.warning(f"Room type with ID {id_} not found for update")
            raise HTTPException(status_code=404, detail="Room type not found")

        if data.description is not None:
            entity.description = data.description
        if data.max_guests is not None:
            entity.max_guests = data.max_guests

        updated = self.repo.update(entity)
        logger.info(f"Room type ID {id_} updated")
        return RoomTypeOut.model_validate(updated)

    def delete(self, id_: int) -> RoomTypeOut:
        logger.info(f"Deleting room type ID {id_}")
        deleted = self.repo.delete(id_)
        logger.info(f"Room type ID {id_} deleted")
        return RoomTypeOut.model_validate(deleted)


def get_room_type_service(db: Session = Depends(get_db)) -> RoomTypeService:
    return RoomTypeService(db=db)
