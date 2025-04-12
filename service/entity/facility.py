from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Facility(Base):
    __tablename__ = "facility"

    facility_id = Column(Integer, primary_key=True, autoincrement=True)
    facility_name = Column(String, nullable=False, index=True)
