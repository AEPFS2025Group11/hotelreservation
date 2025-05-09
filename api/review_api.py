from fastapi import APIRouter, Depends

from app.services.models.review_models import ReviewIn, ReviewOut, ReviewUpdate
from app.services.review_service import ReviewService, get_review_service

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewOut)
async def add_review(review: ReviewIn, service: ReviewService = Depends(get_review_service)):
    return service.create(review)


@router.get("/hotel/{hotel_id}", response_model=list[ReviewOut])
async def get_reviews_by_hotel_id(hotel_id: int, service: ReviewService = Depends(get_review_service)):
    return service.get_by_hotel_id(hotel_id)


@router.get("/{review_id}", response_model=ReviewOut)
async def get_review_by_id(review_id: int, service: ReviewService = Depends(get_review_service)):
    return service.get_by_id(review_id)


@router.get("/bookings/{booking_id}", response_model=ReviewOut | None)
async def get_review_by_booking_id(booking_id: int, service: ReviewService = Depends(get_review_service)):
    return service.get_by_booking_id(booking_id)


@router.put("/{review_id}", response_model=ReviewOut)
async def update_review(review_id: int, data: ReviewUpdate, service: ReviewService = Depends(get_review_service)):
    return service.update(review_id, data)


@router.delete("/{review_id}", response_model=ReviewOut)
def delete_review(review_id: int, service: ReviewService = Depends(get_review_service)):
    return service.delete(review_id)
