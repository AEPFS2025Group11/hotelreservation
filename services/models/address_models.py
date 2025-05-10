from pydantic import BaseModel


class AddressIn(BaseModel):
    street: str
    city: str
    zip_code: str

    model_config = {'from_attributes': True}


class AddressOut(AddressIn):
    id: int
    street: str
    city: str
    zip_code: str
    latitude: float
    longitude: float

    model_config = {'from_attributes': True}
