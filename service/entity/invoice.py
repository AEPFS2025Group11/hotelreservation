from sqlalchemy import Column, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from app.util.base import Base

class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("booking.id"), nullable=False)
    issue_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)

    booking = relationship("Booking", back_populates="invoice")
    payment = relationship("Payment", back_populates="invoice", uselist=False)
