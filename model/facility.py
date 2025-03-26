import uuid

from hotelreservation.model.room import Room


class Facility(object):
    def __init__(self, facility_name: str, room: Room):
        self.__facility_id = uuid.uuid4()
        self.__facility_name = facility_name
        self.__room = room

    @property
    def facility_id(self):
        return self.__facility_id

    @property
    def facility_name(self):
        return self.__facility_name

    @facility_name.setter
    def facility_name(self, value: str):
        self.__facility_name = value

    @property
    def room(self):
        return self.__room

    @room.setter
    def room(self, value: Room):
        self.__room = value
