from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.service.entity.room_facility import room_facility
from app.util.base import Base


class Facility(Base):
    __tablename__ = "facility"

    facility_id = Column(Integer, primary_key=True, autoincrement=True)
    facility_name = Column(String, nullable=False, index=True)

    rooms = relationship(
        "Room",
        secondary=room_facility,
        back_populates="facilities"
    )
