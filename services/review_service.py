import logging
from datetime import datetime

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.review_repository import ReviewRepository
from app.entities import Review
from app.services.models.review_models import ReviewIn, ReviewOut, ReviewUpdate

logger = logging.getLogger(__name__)


class ReviewService:
    def __init__(self, db: Session):
        self.repo = ReviewRepository(db)

    def create(self, data: ReviewIn) -> ReviewOut:
        logger.debug("Attempting to create review for booking %s", data.booking_id)
        existing = self.repo.get_by_booking_id(data.booking_id)
        if existing:
            logger.warning("A review already exists for booking %s", data.booking_id)
            raise HTTPException(status_code=400, detail="Diese Buchung wurde bereits bewertet.")
        review = Review(**data.model_dump())
        review.created_at = datetime.now()
        saved = self.repo.create(review)
        logger.info("Successfully created review with ID %s", saved.id)
        return ReviewOut.model_validate(saved)

    def get_by_hotel_id(self, hotel_id: int) -> list[ReviewOut]:
        logger.debug("Fetching reviews for hotel %s", hotel_id)
        reviews = self.repo.get_by_hotel_id(hotel_id)
        logger.info("Found %d reviews for hotel %s", len(reviews), hotel_id)
        return [ReviewOut.model_validate(r) for r in reviews]

    def get_by_booking_id(self, booking_id: int) -> ReviewOut | None:
        logger.debug("Fetching review for booking %s", booking_id)
        review = self.repo.get_by_booking_id(booking_id)
        if not review:
            logger.warning("No review found for booking %s", booking_id)
            return None
        return ReviewOut.model_validate(review)

    def update(self, review_id: int, data: ReviewUpdate) -> ReviewOut:
        logger.debug("Updating review %s with data: %s", review_id, data.model_dump())
        entity = self.repo.get_by_id(review_id)
        if data.rating is not None:
            entity.rating = data.rating
        if data.comment is not None:
            entity.comment = data.comment
        updated = self.repo.update(entity)
        logger.info("Review %s updated successfully", review_id)
        return ReviewOut.model_validate(updated)

    def delete(self, review_id: int) -> ReviewOut:
        logger.debug("Deleting review %s", review_id)
        deleted = self.repo.delete(review_id)
        logger.info("Review %s deleted successfully", review_id)
        return ReviewOut.model_validate(deleted)

    def get_by_id(self, review_id: int) -> ReviewOut:
        logger.debug("Retrieving review with ID %s", review_id)
        review = self.repo.get_by_id(review_id)
        if not review:
            logger.warning("Review with ID %s not found", review_id)
        return ReviewOut.model_validate(review)


def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
    return ReviewService(db=db)
