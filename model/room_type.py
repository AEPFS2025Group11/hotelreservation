import uuid


class RoomType(object):
    def __init__(self, description: str, max_guests: int):
        self.__room_type_id = uuid.uuid4()
        self.__description = description
        self.__max_guests = max_guests

    @property
    def room_type_id(self):
        return self.__room_type_id

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def max_guests(self):
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, value):
        self.__max_guests = value