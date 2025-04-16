from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer, ForeignKey('guest.guest_id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.room_id'), nullable=False)
    check_in_date = Column(DateTime, nullable=False, index=True)
    check_out_date = Column(DateTime, nullable=False, index=True)
    is_cancelled = Column(Boolean, nullable=False, index=True)
    total_amount = Column(Integer, nullable=False, index=True)
