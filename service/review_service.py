import logging

from fastapi import HTTPException

from app.repository.review_repository import ReviewRepository
from app.service.entity.review import Review
from app.service.models.review_models import ReviewIn, ReviewOut, ReviewUpdate

logger = logging.getLogger(__name__)


class ReviewService:
    def __init__(self, repo: ReviewRepository):
        self.repo = repo

    def create(self, data: ReviewIn) -> ReviewOut:
        existing = self.repo.get_by_booking_id(data.booking_id)
        if existing:
            raise HTTPException(status_code=400, detail="Diese Buchung wurde bereits bewertet.")
        review = Review(**data.model_dump())
        saved = self.repo.create(review)
        return ReviewOut.model_validate(saved)

    def get_by_hotel_id(self, hotel_id: int) -> list[ReviewOut]:
        reviews = self.repo.get_by_hotel_id(hotel_id)
        return [ReviewOut.model_validate(r) for r in reviews]

    def get_by_booking_id(self, booking_id: int) -> ReviewOut:
        reviews = self.repo.get_by_booking_id(booking_id)
        return ReviewOut.model_validate(reviews)

    def update(self, review_id: int, data: ReviewUpdate) -> ReviewOut:
        entity = self.repo.get_by_id(review_id)
        if data.rating is not None:
            entity.rating = data.rating
        if data.comment is not None:
            entity.comment = data.comment
        return ReviewOut.model_validate(self.repo.update(entity))

    def delete(self, id_: int) -> ReviewOut:
        return ReviewOut.model_validate(self.repo.delete(id_))

    def get_by_id(self, id_: int) -> ReviewOut:
        return ReviewOut.model_validate(self.repo.get_by_id(id_))
