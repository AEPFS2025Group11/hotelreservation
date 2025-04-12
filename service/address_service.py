from app.repository.address_repository import AddressRepository
from app.service.dto.address_schema import AddressSchema
from app.service.entity.address import Address
from app.service.mapper.address_mapper import map_to_entity, map_to_dict


class AddressService:
    def __init__(self):
        self.repo = AddressRepository()
        self.schema = AddressSchema()

    def create(self, data: dict) -> dict:
        entity = map_to_entity(self.schema, Address, data)
        saved = self.repo.add(entity)
        return map_to_dict(self.schema, saved)

    def get_all(self) -> list[dict]:
        return [map_to_dict(self.schema, addr) for addr in self.repo.get_all()]
