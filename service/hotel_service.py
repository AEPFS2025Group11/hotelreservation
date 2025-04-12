from app.repository.hotel_repository import HotelRepository
from app.service.dto.hotel_models import HotelOut
from app.service.dto.hotel_schema import HotelSchema


class HotelService:
    def __init__(self):
        self.repo = HotelRepository()
        self.schema = HotelSchema()

    def get_all(self) -> list[HotelOut]:
        hotels = self.repo.get_all()
        return [HotelOut.model_validate(h) for h in hotels]
