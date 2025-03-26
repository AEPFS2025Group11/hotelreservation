import uuid

from hotelreservation.model.facility import Facility
from hotelreservation.model.hotel import Hotel
from hotelreservation.model.room_type import RoomType


class Room(object):
    def __init__(self, hotel: Hotel, room_number: int, room_type: RoomType, facility: Facility):
        self.__room_id = uuid.uuid4()
        self.__hotel = hotel
        self.__room_number = room_number
        self.__room_type = room_type
        self.__facility = facility

    @property
    def room_id(self):
        return self.__room_id

    @property
    def hotel(self):
        return self.__hotel

    @hotel.setter
    def hotel(self, value: Hotel):
        self.__hotel = value

    @property
    def room_number(self):
        return self.__room_number

    @room_number.setter
    def room_number(self, value: int):
        if not isinstance(value, int):
            raise TypeError('Room number must be an integer')
        self.__room_number = value

    @property
    def room_type(self):
        return self.__room_type

    @room_type.setter
    def room_type(self, value: RoomType):
        self.__room_type = value

    @property
    def facility(self):
        return self.__facility

    @facility.setter
    def facility(self, value: Facility):
        self.__facility = value