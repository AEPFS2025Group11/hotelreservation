from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.util.base import Base
from app.util.enums import InvoiceStatus


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    check_in = Column(Date, nullable=False, index=True)
    check_out = Column(Date, nullable=False, index=True)
    is_cancelled = Column(Boolean, nullable=False, index=True)
    total_amount = Column(Integer, nullable=False, index=True)

    user = relationship("User", back_populates="bookings", lazy="joined")
    room = relationship("Room", back_populates="bookings", lazy="joined")

    invoice = relationship("Invoice", back_populates="booking", uselist=False, cascade="all, delete-orphan")
    payments = relationship(
        "Payment",
        back_populates="booking",
        cascade="all, delete-orphan"
    )
    review = relationship('Review', back_populates='booking', cascade='all, delete', passive_deletes=True)

    @property
    def is_paid(self) -> bool:
        if not self.invoice or self.invoice.status != InvoiceStatus.PAID:
            return False

        total_paid = sum(p.amount for p in self.payments)
        return total_paid >= self.invoice.total_amount

    @property
    def has_review(self) -> bool:
        if not self.review:
            return False
        else:
            return True
