from dataclasses import dataclass, field
import uuid

@dataclass
class Address:
    address_id: uuid.UUID = field(default_factory=uuid.uuid4)
    street: str = ""
    city: str = ""
    zip_code: str = ""
