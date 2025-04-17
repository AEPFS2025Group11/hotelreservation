from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum
from app.util.base import Base
from app.util.enums import Gender


class Guest(Base):
    __tablename__ = "guest"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(50), nullable=False, index=True)
    phone_number = Column(String(20), nullable=True)
    birth_date = Column(Date, nullable=False, index=True)
    nationality = Column(String, nullable=False, index=True)
    gender = Column(SqlEnum(Gender), nullable=False, index=True)
    loyalty_points = Column(Integer, default=0)

    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    address = relationship("Address", back_populates="guests", lazy="joined")

    bookings = relationship("Booking", back_populates="guest", lazy="joined")

    reviews = relationship("Review", back_populates="guest", cascade="all, delete-orphan")
