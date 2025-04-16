from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.util.base import Base


class Room(Base):
    __tablename__ = "room"

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey('hotel.hotel_id'), nullable=False)
    room_number = Column(Integer, nullable=False, index=True)
    type_id = Column(Integer, ForeignKey('room_type.type_id'), nullable=False)
    price_per_night = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)

    hotel = relationship("Hotel", back_populates="rooms", lazy="joined")

    type = relationship("RoomType", lazy="joined")
