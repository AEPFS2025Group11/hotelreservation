from app.business_layer.entity.facility import Facility
from app.util.database import SessionLocal


class FacilityRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Facility).all()

    def get_by_id(self, facility_id: int):
        return self.db.query().filter(Facility.facility_id == facility_id).first()
