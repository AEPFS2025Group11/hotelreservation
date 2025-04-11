from app.data_access_layer.database import SessionLocal
from app.data_access_layer.entity.address import Address


class AddressRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Address).all()

    def get_address_by_id(self, id: int):
        return self.db.query(Address).filter(Address.address_id == id).first()

    def add_user(self, street: str, city: str, zipcode: str):
        new_user = Address(street=street, city=city, zip_code=zipcode)
        self.db.add(new_user)
        self.db.commit()
        return new_user
