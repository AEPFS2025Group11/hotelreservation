from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.repository.base_repository import BaseRepository
from app.service.entity.review import Review


class ReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal(), Review)

    def get_by_hotel_id(self, hotel_id: int) -> list[Review]:
        return self.db.query(self.model).filter(self.model.hotel_id == hotel_id).all()

    def get_all(self):
        return (
            self.db.query(self.model)
            .options(joinedload(self.model.guest), joinedload(self.model.hotel))
            .all()
        )

    def get_by_id(self, id_: int):
        review = (
            self.db.query(self.model)
            .options(joinedload(self.model.guest), joinedload(self.model.hotel))
            .filter(self.model.id == id_)
            .first()
        )
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review
