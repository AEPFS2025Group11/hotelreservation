import uuid

from hotelreservation.model.booking import Booking


class Invoice(object):
    def __init__(self, booking: Booking, issue_date: str, total_amount: float):
        self.__invoice_id = uuid.uuid4()
        self.__booking = booking
        self.__issue_date = issue_date
        self.__total_amount = total_amount

    @property
    def invoice_id(self):
        return self.__invoice_id

    @property
    def booking(self):
        return self.__booking

    @booking.setter
    def booking(self, value: Booking):
        self.__booking = value

    @property
    def issue_date(self):
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: str):
        self.__issue_date = value

    @property
    def total_amount(self):
        return self.__total_amount

    @total_amount.setter
    def total_amount(self, value: float):
        self.__total_amount = value