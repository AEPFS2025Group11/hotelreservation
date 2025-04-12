from fastapi import APIRouter

from app.service.dto.hotel_models import HotelOut
from app.service.hotel_service import HotelService

router = APIRouter(prefix="/api", tags=["hotels"])
hotel_service = HotelService()


@router.get("/hotels", response_model=list[HotelOut])
async def get_addresses():
    return hotel_service.get_all()
