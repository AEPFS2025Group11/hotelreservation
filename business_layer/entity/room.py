from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Room(Base):
    __tablename__ = "room"

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, nullable=False, foreign_key=True)
    room_number = Column(Integer, nullable=False)
    type_id = Column(Integer, nullable=False, foreign_key=True)
    price_per_night = Column(Integer, nullable=False)
