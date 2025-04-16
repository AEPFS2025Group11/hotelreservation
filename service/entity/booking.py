from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date

from app.util.base import Base


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer, ForeignKey('guest.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    check_in = Column(Date, nullable=False, index=True)
    check_out = Column(Date, nullable=False, index=True)
    is_cancelled = Column(Boolean, nullable=False, index=True)
    total_amount = Column(Integer, nullable=False, index=True)
