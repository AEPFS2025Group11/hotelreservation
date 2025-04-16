from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from app.util.base import Base


@dataclass
class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    zip_code = Column(String, nullable=False, index=True)
