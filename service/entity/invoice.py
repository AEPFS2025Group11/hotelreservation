from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.util.base import Base

class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    issue_date = Column(Date, nullable=False)
    total_amount = Column(Integer, nullable=False)

    booking = relationship("Booking", back_populates="invoice")
