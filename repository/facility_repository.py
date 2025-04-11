from app.data_access_layer.database import SessionLocal
from app.data_access_layer.entity.facility import Facility


class FacilityRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Facility).all()

    def get_by_id(self, facility_id: int):
        return self.db.query().filter(Facility.facility_id == facility_id).first()
