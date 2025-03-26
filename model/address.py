import uuid
class Address(object):
    _address_id = uuid.uuid4()
    _street = ""
    _city = ""
    _zip_code = ""

    def __init__(self, street, city, zip_code):
        self._street = street
        self._city = city
        self._zip_code = zip_code

