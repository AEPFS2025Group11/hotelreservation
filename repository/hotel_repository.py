from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.dto.hotel_models import HotelIn, HotelUpdate
from app.service.entity.address import Address
from app.service.entity.hotel import Hotel


class HotelRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self) -> list[Hotel]:
        return self.db.query(Hotel).options(joinedload(Hotel.address)).all()

    def get_by_id(self, hotel_id: int) -> Hotel:
        return self.db.query(Hotel).options(joinedload(Hotel.address)).filter(Hotel.hotel_id == hotel_id).first()

    def create(self, hotel_data: HotelIn) -> Hotel:
        address = self.db.query(Address).filter_by(address_id=hotel_data.address_id).first()

        if address is None:
            raise HTTPException(status_code=404, detail="Address not found")

        hotel = Hotel(name=hotel_data.name, stars=hotel_data.stars, address_id=address.address_id)
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def update(self, hotel_id: int, data: HotelUpdate) -> Hotel:
        hotel = self.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        if data.name is not None:
            hotel.name = data.name
        if data.stars is not None:
            hotel.stars = data.stars
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def delete(self, hotel_id: int) -> Hotel:
        hotel = self.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        self.db.delete(hotel)
        self.db.commit()
        return hotel
