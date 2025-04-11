from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoice"

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, foreign_key=True)
    issue_date = Column(DateTime, nullable=False)
    total_amount = Column(Integer, nullable=False)