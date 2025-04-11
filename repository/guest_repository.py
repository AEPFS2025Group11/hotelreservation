from app.data_access_layer.database import SessionLocal
from app.data_access_layer.entity.guest import Guest


class GuestRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Guest).all()

    def get_by_id(self, guest_id: int):
        return self.db.query().filter(Guest.guest_id == guest_id).first()
