from typing import Optional

from fastapi import HTTPException

from app.repository.address_repository import AddressRepository
from app.repository.hotel_repository import HotelRepository
from app.service.dto.hotel_models import HotelOut, HotelIn, HotelUpdate
from app.service.entity.hotel import Hotel


class HotelService:
    def __init__(self):
        self.hotel_repo = HotelRepository()
        self.address_repo = AddressRepository()

    def get_filtered(self, city: Optional[str] = None, min_stars: Optional[int] = None) -> list[HotelOut]:
        hotels = self.hotel_repo.get_filtered(city, min_stars)
        return [HotelOut.model_validate(h) for h in hotels]

    def get_by_id(self, hotel_id: int) -> HotelOut:
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return HotelOut.model_validate(hotel)

    def create(self, hotel_data: HotelIn) -> HotelOut:
        hotel = self.hotel_repo.create(hotel_data)
        return HotelOut.model_validate(hotel)

    def update(self, hotel_id: int, update_data: HotelUpdate) -> HotelOut:
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return HotelOut.model_validate(self.hotel_repo.update(hotel_id, update_data))

    def delete(self, hotel_id: int) -> Hotel:
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return self.hotel_repo.delete(hotel_id)
