import logging

from app.entities.address import Address
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AddressRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Address)

    def get_by_name(self, city: str) -> list[Address]:
        logger.info(f"Fetching addresses by city: {city}")
        addresses = self.db.query(self.model).filter(self.model.city == city).all()
        logger.info(f"Found {len(addresses)} address(es) in city {city}")
        return addresses
