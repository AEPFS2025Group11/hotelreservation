from fastapi import HTTPException

from app.repository.hotel_repository import HotelRepository
from app.service.dto.hotel_models import HotelOut, HotelIn, HotelUpdate
from app.service.entity.hotel import Hotel


class HotelService:
    def __init__(self):
        self.repo = HotelRepository()

    def get_all(self) -> list[HotelOut]:
        hotels = self.repo.get_all()
        return [HotelOut.model_validate(h) for h in hotels]

    def get_by_id(self, hotel_id: int) -> HotelOut:
        hotel = self.repo.get_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return HotelOut.model_validate(hotel)

    def create(self, hotel_data: HotelIn) -> HotelOut:
        hotel = self.repo.create(hotel_data)
        return HotelOut.model_validate(hotel)

    def update(self, hotel_id: int, update_data: HotelUpdate) -> HotelOut:
        hotel = self.repo.update(hotel_id, update_data)
        return HotelOut.model_validate(hotel)

    def delete(self, hotel_id: int) -> Hotel:
        return self.repo.delete(hotel_id)
