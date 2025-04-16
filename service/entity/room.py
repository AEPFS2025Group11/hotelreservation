from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship

from app.service.entity.room_facility import room_facility
from app.util.base import Base


class Room(Base):
    __tablename__ = "room"

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey('hotel.hotel_id'), nullable=False)
    room_number = Column(String, nullable=False, index=True)
    type_id = Column(Integer, ForeignKey('room_type.type_id'), nullable=False)
    price_per_night = Column(Float, nullable=False)

    hotel = relationship("Hotel", back_populates="rooms", lazy="joined")

    type = relationship("RoomType", lazy="joined")

    facilities = relationship(
        "Facility",
        secondary=room_facility,
        back_populates="rooms"
    )
