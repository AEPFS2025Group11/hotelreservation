from pydantic import BaseModel


class AddressIn(BaseModel):
    street: str
    city: str
    zip_code: str

    model_config = {'from_attributes': True}


class AddressOut(AddressIn):
    address_id: int

    model_config = {'from_attributes': True}
