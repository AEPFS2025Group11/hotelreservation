from fastapi import APIRouter

from app.service.address_service import AddressService
from app.service.models.address_models import AddressOut, AddressIn

router = APIRouter(prefix="/api", tags=["addresses"])
address_service = AddressService()


@router.get("/addresses", response_model=list[AddressOut])
async def get_addresses():
    return address_service.get_all()


@router.post("/addresses", response_model=AddressOut)
async def create_address(address: AddressIn):
    return address_service.create(address.model_dump())
