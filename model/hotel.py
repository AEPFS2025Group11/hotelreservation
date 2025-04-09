import uuid

from app.model.address import Address


class Hotel(object):
    def __init__(self, name: str, stars: str, address: Address):
        self.__hotel_id = uuid.uuid4()
        self.__name = name
        self.__stars = stars
        self.__address = address

    @property
    def hotel_id(self):
        return self.__hotel_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def stars(self):
        return self.__stars

    @stars.setter
    def stars(self, value: str):
        self.__stars = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value: Address):
        self.__address = value
