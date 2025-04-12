import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException

from app.business_layer.address_service import AddressService
from app.business_layer.dto.address_models import AddressOut, AddressIn

app = FastAPI()
address_service = AddressService()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/addresses", response_model=list[AddressOut])
def get_addresses():
    return address_service.get_all()


@app.post("/addresses", response_model=AddressOut)
def create_address(address: AddressIn):
    try:
        return address_service.create(address.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# at last, the bottom of the file/module
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
