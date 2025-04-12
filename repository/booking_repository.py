from app.database.database import SessionLocal
from app.service.entity.booking import Booking


class BookingRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Booking).all()

    def get_by_id(self, booking_id: int):
        return self.db.query(Booking).filter(Booking.booking_id == booking_id).first()
