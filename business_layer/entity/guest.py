from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Guest(Base):
    __tablename__ = "guest"

    guest_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(50), nullable=False, index=True)
    address_id = Column(Integer, nullable=False, foreign_key=True)
