from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from app.util.base import Base


class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("booking.id"), nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoice.id"), nullable=True)
    method = Column(String, nullable=False)
    status = Column(String, nullable=False)
    paid_at = Column(DateTime)
    amount = Column(Float, nullable=False)

    booking = relationship("Booking", back_populates="payments")
    invoice = relationship("Invoice", back_populates="payment")
