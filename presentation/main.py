from fastapi import FastAPI, HTTPException

from app.business_layer.address_service import AddressService
from app.business_layer.dto.address_models import AddressOut, AddressIn

app = FastAPI()
service = AddressService()


@app.get("/addresses", response_model=list[AddressOut])
def get_addresses():
    return service.get_all()


@app.post("/addresses", response_model=AddressOut)
def create_address(address: AddressIn):
    try:
        return service.create(address.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


address_service = AddressService()

data = address_service.get_all()

print(data)
