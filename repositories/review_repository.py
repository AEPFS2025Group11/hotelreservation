from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from app.entities import Review, Booking, Room
from app.repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Review)

    def get_by_hotel_id(self, hotel_id: int) -> list[Review]:
        return (
            self.db.query(self.model)
            .join(self.model.booking)
            .join(Booking.room)
            .join(Room.hotel)
            .filter(Room.hotel_id == hotel_id)
            .all()
        )

    def get_by_booking_id(self, booking_id: int) -> Review:
        return self.db.query(self.model).filter(self.model.booking_id == booking_id).first()

    def get_all(self):
        return (
            self.db.query(self.model)
            .options(joinedload(self.model.user), joinedload(self.model.hotel))
            .all()
        )

    def get_by_id(self, id_: int):
        review = (
            self.db.query(self.model)
            .options(joinedload(self.model.user), joinedload(self.model.hotel))
            .filter(self.model.id == id_)
            .first()
        )
        if not review:
            raise HTTPException(status_code=404, detail="Review konnte nicht gefunden werden.")
        return review
