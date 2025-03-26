import uuid

from paprika import *


@data
class Address(object):
    __address_id = uuid.uuid4()
    __number: int
    __street: str
    __city: str
    __zip_code: str

    def __init__(self, street, city, zip_code):
        self.__street = street
        self.__city = city
        self.__zip_code = zip_code

    @property
    def __number(self):
        return self.__number

    @__number.setter
    def __number(self, value):
        try:
            self.__number = int(value)
        except ValueError:
            print("Invalid number")

    @property
    def __street(self):
        return self.__street

    @__street.setter
    def __street(self, value):
        self.__street = value

    @property
    def __city(self):
        return self.__city

    @__city.setter
    def __city(self, value):
        self.__city = value

    @property
    def __zip_code(self):
        return self.__zip_code

    @__zip_code.setter
    def __zip_code(self, value):
        self.__zip_code = value
