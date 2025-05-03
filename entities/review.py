from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app.util.base import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("booking.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    comment = Column(Text, nullable=True)

    booking = relationship("Booking", back_populates="review")
