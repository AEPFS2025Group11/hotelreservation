import uuid

from hotelreservation.model.address import Address


class Guest(object):
    def __init__(self, first_name: str, last_name: str, email: str, address: Address):
        self.__guest_id = uuid.uuid4()
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__address = address

    @property
    def address_id(self):
        return self.__guest_id

    @property
    def street(self):
        return self.__first_name

    @street.setter
    def street(self, value: str):
        self.__first_name = value

    @property
    def city(self):
        return self.__last_name

    @city.setter
    def city(self, value: str):
        self.__last_name = value

    @property
    def zip_code(self):
        return self.__email

    @zip_code.setter
    def zip_code(self, value: str):
        self.__email = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value