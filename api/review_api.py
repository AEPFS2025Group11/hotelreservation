from functools import lru_cache

from fastapi import APIRouter, Depends

from app.repository.review_repository import ReviewRepository
from app.service.models.review_models import ReviewIn, ReviewOut, ReviewUpdate
from app.service.review_service import ReviewService

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@lru_cache()
def get_service() -> ReviewService:
    return ReviewService(ReviewRepository())


@router.post("/", response_model=ReviewOut)
async def add_review(review: ReviewIn, service: ReviewService = Depends(get_service)):
    return service.create(review)


@router.get("/hotel/{hotel_id}", response_model=list[ReviewOut])
async def get_reviews(hotel_id: int, service: ReviewService = Depends(get_service)):
    return service.get_by_hotel_id(hotel_id)


@router.get("/{review_id}", response_model=ReviewOut)
def get_by_id(review_id: int, service: ReviewService = Depends(get_service)):
    return service.get_by_id(review_id)


@router.get("/bookings/{booking_id}", response_model=ReviewOut)
def get_by_booking_id(booking_id: int, service: ReviewService = Depends(get_service)):
    return service.get_by_booking_id(booking_id)


@router.put("/{review_id}", response_model=ReviewOut)
def update(review_id: int, data: ReviewUpdate, service: ReviewService = Depends(get_service)):
    return service.update(review_id, data)


@router.delete("/{review_id}", response_model=ReviewOut)
def delete(review_id: int, service: ReviewService = Depends(get_service)):
    return service.delete(review_id)
