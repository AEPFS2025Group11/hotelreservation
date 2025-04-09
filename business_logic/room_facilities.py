from app.data_access.room_facilities_dal import *

def get_all():
    data = get_all_data()
    return data