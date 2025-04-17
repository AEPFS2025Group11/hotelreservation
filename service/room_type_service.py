# app/service/room_type_service.py
import logging

from app.repository.room_type import RoomTypeRepository
from app.service.models.room_type_models import RoomTypeIn, RoomTypeOut

logger = logging.getLogger(__name__)


class RoomTypeService:
    def __init__(self, repo: RoomTypeRepository):
        self.repo = repo

    def get_all(self) -> list[RoomTypeOut]:
        room_types = self.repo.get_all()
        return [RoomTypeOut.model_validate(r) for r in room_types]

    def get_by_id(self, id_: int) -> RoomTypeOut:
        rt = self.repo.get_by_id(id_)
        return RoomTypeOut.model_validate(rt)

    def create(self, data: RoomTypeIn) -> RoomTypeOut:
        logger.info(f"Creating room type: {data.description}")
        entity = self.repo.model(**data.model_dump())
        return RoomTypeOut.model_validate(self.repo.create(entity))

    def update(self, id_: int, data: RoomTypeIn) -> RoomTypeOut:
        entity = self.repo.get_by_id(id_)
        if data.description:
            entity.description = data.description
        if data.max_guests:
            entity.max_guests = data.max_guests
        return RoomTypeOut.model_validate(self.repo.update(entity))

    def delete(self, id_: int) -> RoomTypeOut:
        return RoomTypeOut.model_validate(self.repo.delete(id_))
