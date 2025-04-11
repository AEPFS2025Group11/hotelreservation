from pydantic import BaseModel


class AddressIn(BaseModel):
    street: str
    city: str
    zipcode: str


class AddressOut(AddressIn):
    id: int
