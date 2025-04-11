from app.business_layer.entity.address import Address
from app.util.database import SessionLocal


class AddressRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Address).all()

    def get_by_id(self, address_id: int):
        return self.db.query(Address).filter(Address.address_id == address_id).first()

    def add(self, address: Address):
        self.db.add(address)
        self.db.commit()
        return address
