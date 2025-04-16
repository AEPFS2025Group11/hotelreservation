import logging

from app.repository.address_repository import AddressRepository
from app.service.models.address_models import AddressIn, AddressOut

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AddressService:
    def __init__(
            self,
            address_repo: AddressRepository,
    ):
        self.address_repo = address_repo

    def create(self, hotel_data: AddressIn) -> AddressOut:
        logger.info(f"Creating hotel: {hotel_data.name}")
        hotel = self.address_repo.create(hotel_data)
        return AddressOut.model_validate(hotel)

    def get_all(self) -> list[AddressOut]:
        return [AddressOut.model_validate(addr) for addr in self.address_repo.get_all()]
