from functools import lru_cache

from fastapi import APIRouter, Depends

from app.repository.booking_repository import BookingRepository
from app.repository.invoice_repository import InvoiceRepository
from app.service.invoice_service import InvoiceService
from app.service.models.invoice_models import InvoiceOut

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


@lru_cache()
def get_invoice_service() -> InvoiceService:
    return InvoiceService(invoice_repo=InvoiceRepository(), booking_repo=BookingRepository())


@router.get("/", response_model=list[InvoiceOut])
async def get_all(service: InvoiceService = Depends(get_invoice_service)):
    return service.get_all()


@router.get("/{invoice_id}", response_model=InvoiceOut)
async def get_invoice(invoice_id: int, service: InvoiceService = Depends(get_invoice_service)):
    return service.get_by_id(invoice_id)
