from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from app.util.base import Base


class RoomType(Base):
    __tablename__ = "room_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False, index=True)
    max_guests = Column(Integer, nullable=False, index=True)
