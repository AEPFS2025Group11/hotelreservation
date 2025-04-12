from app.database.database import SessionLocal
from app.service.entity.hotel import Hotel


class HotelRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Hotel).all()

    def get_by_id(self, hotel_id: int):
        return self.db.query().filter(Hotel.hotel_id == hotel_id).first()
