from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.util.base import Base


@dataclass
class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    stars = Column(Integer, nullable=False, index=True)

    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    address = relationship("Address", back_populates="hotel", uselist=False, lazy="joined")

    rooms = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")
