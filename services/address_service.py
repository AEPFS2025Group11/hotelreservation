import logging

from app.repositories.address_repository import AddressRepository
from app.entities.address import Address
from app.services.models.address_models import AddressIn, AddressOut

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AddressService:
    def __init__(self, address_repo: AddressRepository):
        self.address_repo = address_repo

    def create(self, data: AddressIn) -> AddressOut:
        logger.info(f"Creating new address: {data.model_dump()}")
        address = Address(**data.model_dump())
        saved = self.address_repo.create(address)
        logger.info(f"Address created successfully with ID {saved.id}")
        return AddressOut.model_validate(saved)

    def get_all(self) -> list[AddressOut]:
        logger.info("Fetching all addresses")
        addresses = self.address_repo.get_all()
        logger.info(f"{len(addresses)} address(es) found")
        return [AddressOut.model_validate(addr) for addr in addresses]
