from app.repository.address_repository import AddressRepository


class AddressService:
    def __init__(self):
        self.repo = AddressRepository()

    def get_all(self):
        return self.repo.get_all()

    def create(self, street: str, city: str, zipcode: str):
        if not street or not city or not zipcode:
            raise ValueError("Street, city, zipcode are required")
        return self.repo.add(street=street, city=city, zipcode=zipcode)
