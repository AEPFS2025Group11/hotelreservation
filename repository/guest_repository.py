from app.database.database import SessionLocal
from app.service.entity.guest import Guest


class GuestRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Guest).all()

    def get_by_id(self, guest_id: int):
        return self.db.query().filter(Guest.id == guest_id).first()
