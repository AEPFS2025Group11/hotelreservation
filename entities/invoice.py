from sqlalchemy import Column, Integer, ForeignKey, Date, Float
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.util.base import Base
from app.util.enums import InvoiceStatus


class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("booking.id"), nullable=False)
    issue_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(SqlEnum(InvoiceStatus), nullable=False, default="pending")

    booking = relationship("Booking", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")

    @property
    def amount_to_pay(self):
        return self.total_amount - sum(payment.amount for payment in self.payments)

    @property
    def is_paid(self) -> bool:
        return self.amount_to_pay <= 0
