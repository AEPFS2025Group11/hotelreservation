from app.database.database import SessionLocal
from app.service.entity.facility import Facility


class FacilityRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Facility).all()

    def get_by_id(self, facility_id: int):
        return self.db.query().filter(Facility.id == facility_id).first()
