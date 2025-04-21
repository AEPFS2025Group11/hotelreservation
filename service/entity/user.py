from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.util.base import Base
from app.util.enums import Role, Gender


@dataclass
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(Role), nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    phone_number = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    nationality = Column(String, nullable=True)
    gender = Column(SqlEnum(Gender), nullable=True)
    loyalty_points = Column(Integer, nullable=True)

    bookings = relationship("Booking", back_populates="user", lazy="joined")

    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    address = relationship("Address", back_populates="users")
