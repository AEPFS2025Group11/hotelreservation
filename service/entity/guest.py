from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.util.base import Base


class Guest(Base):
    __tablename__ = "guest"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(50), nullable=False, index=True)
    phone_number = Column(String(20), nullable=True)

    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    address = relationship("Address", back_populates="guests", lazy="joined")

    bookings = relationship("Booking", back_populates="guest", lazy="joined")
