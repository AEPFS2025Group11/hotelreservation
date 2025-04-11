from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.model.address import Address
from app.model.guest import Guest

Base = declarative_base()

engine = create_engine("sqlite:///../database/hotel_reservation_sample.db")  # Use the SQLite driver

print("Connected to database:", engine)

Base.metadata.create_all(engine)
print("Tables created successfully")

session = Session(bind=engine)
print("Session created successfully")

print("User added successfully")
