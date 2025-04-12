from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.entity.hotel import Hotel


class HotelRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self) -> list[Hotel]:
        return self.db.query(Hotel).options(joinedload(Hotel.address)).all()

    def get_by_id(self, hotel_id: int) -> Hotel:
        return self.db.query().filter(Hotel.hotel_id == hotel_id).first()