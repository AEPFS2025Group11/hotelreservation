from app.data_access.hotel_dal import *

def get_all():
    data = get_all_data()
    return data