from app.entities import Facility
from app.repositories.base_repository import BaseRepository


class FacilityRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Facility)

    def get_by_ids(self, facility_ids):
        return self.db.query(self.model).filter(self.model.id.in_(facility_ids)).all()
