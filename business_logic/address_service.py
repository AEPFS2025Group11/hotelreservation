from app.data_access.address_dal import *


def get_all():
    data = get_all_addresses()
    return data


def get_cities():
    data = get_all_addresses()
    address_list = []
    for address in data:
        address_list.append(address.city)
    return address_list
