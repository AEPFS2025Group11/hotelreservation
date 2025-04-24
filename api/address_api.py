from functools import lru_cache
import logging

from fastapi import APIRouter, Depends

from app.repositories.address_repository import AddressRepository
from app.services.address_service import AddressService
from app.services.models.address_models import AddressOut, AddressIn

router = APIRouter(prefix="/api/addresses", tags=["addresses"])
logger = logging.getLogger(__name__)


@lru_cache()
def get_address_service() -> AddressService:
    logger.info("Initializing AddressService via lru_cache")
    return AddressService(address_repo=AddressRepository())


@router.get("/", response_model=list[AddressOut])
async def get_addresses(service: AddressService = Depends(get_address_service)):
    logger.info("GET /api/addresses - Fetching all addresses")
    return service.get_all()


@router.post("/", response_model=AddressOut)
async def create_address(address: AddressIn, service: AddressService = Depends(get_address_service)):
    logger.info(f"POST /api/addresses - Creating address for city: {address.city}")
    return service.create(address)
