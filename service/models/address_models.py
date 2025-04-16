from pydantic import BaseModel


class AddressIn(BaseModel):
    street: str
    city: str
    zip_code: str

    model_config = {'from_attributes': True}


class AddressOut(AddressIn):
    id: int

    model_config = {'from_attributes': True}
