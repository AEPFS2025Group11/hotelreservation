import logging

from fastapi import Depends
from geopy import Nominatim
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.entities.address import Address
from app.repositories.address_repository import AddressRepository
from app.services.models.address_models import AddressIn, AddressOut

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AddressService:
    def __init__(self, db: Session):
        self.address_repo = AddressRepository(db=db)

    def create(self, data: AddressIn) -> AddressOut:
        logger.info(f"Creating new address: {data.model_dump()}")
        lat, lng = geocode_address(data)
        address = Address(**data.model_dump(), latitude=lat, longitude=lng)
        saved = self.address_repo.create(address)
        logger.info(f"Address created successfully with ID {saved.id}")
        return AddressOut.model_validate(saved)

    def get_all(self) -> list[AddressOut]:
        logger.info("Fetching all addresses")
        addresses = self.address_repo.get_all()
        logger.info(f"{len(addresses)} address(es) found")
        return [AddressOut.model_validate(addr) for addr in addresses]


def geocode_address(address: AddressIn) -> tuple[float, float] | tuple[None, None]:
    full_address = f"{address.street}, {address.postal_code} {address.city}, {address.country}"
    geolocator = Nominatim(user_agent="hotel-map")
    location = geolocator.geocode(full_address)
    if location:
        return location.latitude, location.longitude
    return None, None


def get_address_service(db: Session = Depends(get_db)) -> AddressService:
    return AddressService(db=db)
