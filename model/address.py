import uuid

class Address(object):
    def __init__(self, street: str, city: str, zip_code: str):
        self.__address_id = uuid.uuid4()
        self.__street = street
        self.__city = city
        self.__zip_code = zip_code

    @property
    def address_id(self):
        return self.__address_id

    @property
    def street(self):
        return self.__street

    @street.setter
    def street(self, value: str):
        self.__street = value

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value: str):
        self.__city = value

    @property
    def zip_code(self):
        return self.__zip_code

    @zip_code.setter
    def zip_code(self, value: str):
        self.__zip_code = value