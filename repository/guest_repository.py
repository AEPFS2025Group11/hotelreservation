from app.business_layer.entity.guest import Guest
from app.util.database import SessionLocal


class GuestRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Guest).all()

    def get_by_id(self, guest_id: int):
        return self.db.query().filter(Guest.guest_id == guest_id).first()
