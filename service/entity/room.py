from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.util.base import Base
from app.service.entity.room_facility import room_facility


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey('hotel.id'), nullable=False)
    room_number = Column(String, nullable=False, index=True)
    type_id = Column(Integer, ForeignKey('room_type.id'), nullable=False)
    price_per_night = Column(Float, nullable=False)

    hotel = relationship("Hotel", back_populates="rooms", lazy="joined")
    type = relationship("RoomType", lazy="joined")

    bookings = relationship("Booking", back_populates="room")

    facilities = relationship(
        "Facility",
        secondary=room_facility,
        back_populates="rooms"
    )