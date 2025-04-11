from mapper.object_mapper import ObjectMapper

from app.data_access.hotel_dal import *

mapper = ObjectMapper()


def get_all():
    data = get_all_data()
    return mapper.map(data)


def get_hotels_by_city(city):
    data = get_by_city(city)

    return data
