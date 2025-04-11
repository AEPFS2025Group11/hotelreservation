from app.data_access.address_dal import *


def get_all():
    data = get_all_addresses()
    return data


def get_cities():
    data = get_all_addresses()
    address_list = []
    for address in data:
        if address.city not in address_list:
            address_list.append(address.city)
    address_list.sort()
    return address_list
