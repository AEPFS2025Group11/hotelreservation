from typing import Optional

from pydantic import BaseModel, Field


class ReviewIn(BaseModel):
    hotel_id: int
    guest_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewOut(BaseModel):
    id: int
    rating: int
    comment: Optional[str]
    guest_id: int
    hotel_id: int

    model_config = {'from_attributes': True}


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None
