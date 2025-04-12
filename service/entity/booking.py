from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer, nullable=False, foreign_key=True)
    room_id = Column(Integer, nullable=False, foreign_key=True)
    check_in_date = Column(DateTime, nullable=False, index=True)
    check_out_date = Column(DateTime, nullable=False, index=True)
    is_cancelled = Column(Boolean, nullable=False, index=True)
    total_amount = Column(Integer, nullable=False, index=True)
