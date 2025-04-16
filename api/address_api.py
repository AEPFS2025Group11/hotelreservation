from functools import lru_cache

from fastapi import APIRouter, Depends

from app.repository.address_repository import AddressRepository
from app.service.address_service import AddressService
from app.service.models.address_models import AddressOut, AddressIn

router = APIRouter(prefix="/api/addresses", tags=["addresses"])


@lru_cache()
def get_address_service() -> AddressService:
    return AddressService(address_repo=AddressRepository())

@router.get("/", response_model=list[AddressOut])
async def get_addresses(service: AddressService = Depends(get_address_service)):
    return service.get_all()


@router.post("/", response_model=AddressOut)
async def create_address(address: AddressIn, service: AddressService = Depends(get_address_service)):
    return service.create(address)
