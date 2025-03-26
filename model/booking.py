import uuid

from hotelreservation.model.address import Address
from hotelreservation.model.guest import Guest
from hotelreservation.model.room import Room


class Booking(object):
    def __init__(self, guest: Guest, room: Room, check_in_date: str, check_out_date: str, total_amount: float,
                 is_cancelled: bool = False):
        self.__booking_id = uuid.uuid4()
        self.__guest = guest
        self.__room = room
        self.__check_in_date = check_in_date
        self.__check_out_date = check_out_date
        self.__total_amount = total_amount
        self.__is_cancelled = is_cancelled

    @property
    def booking_id(self):
        return self.__booking_id

    @property
    def guest(self):
        return self.__guest

    @guest.setter
    def guest(self, value: Guest):
        self.__guest = value
    @property
    def room(self):
        return self.__room

    @room.setter
    def room(self, value: Room):
        self.__room = value

    @property
    def check_in_date(self):
        return self.__check_in_date

    @check_in_date.setter
    def check_in_date(self, value: str):
        self.__check_in_date = value

    @property
    def check_out_date(self):
        return self.__check_out_date

    @check_out_date.setter
    def check_out_date(self, value: str):
        self.__check_out_date = value

    @property
    def total_amount(self):
        return self.__total_amount

    @total_amount.setter
    def total_amount(self, value: float):
        self.__total_amount = value

    @property
    def is_cancelled(self):
        return self.__is_cancelled

    @is_cancelled.setter
    def is_cancelled(self, value: bool):
        self.__is_cancelled = value