from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.util.base import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    guest_id = Column(Integer, ForeignKey("guest.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    hotel = relationship("Hotel", back_populates="reviews")
    guest = relationship("Guest", back_populates="reviews")
