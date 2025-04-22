from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.util.base import Base
from app.service.entity.room_facility import room_facility


class Facility(Base):
    __tablename__ = "facility"

    id = Column(Integer, primary_key=True, autoincrement=True)
    facility_name = Column(String, nullable=False)

    rooms = relationship(
        "Room",
        secondary=room_facility,
        back_populates="facilities"
    )
