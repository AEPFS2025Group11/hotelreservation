from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hotel(Base):
    __tablename__ = "hotel"

    hotel_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    stars = Column(Integer, nullable=False)
    address_id = Column(Integer, nullable=False, foreign_key=True)
