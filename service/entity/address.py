from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    zip_code = Column(String, nullable=False, index=True)
