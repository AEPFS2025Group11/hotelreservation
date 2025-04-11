from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RoomType(Base):
    __tablename__ = "room_type"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    max_guests = Column(Integer, nullable=False)