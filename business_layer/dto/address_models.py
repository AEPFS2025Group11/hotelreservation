from pydantic import BaseModel


class AddressIn(BaseModel):
    street: str
    city: str
    zip_code: str


class AddressOut(AddressIn):
    address_id: int
