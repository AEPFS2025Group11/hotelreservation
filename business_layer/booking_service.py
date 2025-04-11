from app.data_access_layer.booking_dal import *

def get_all():
    data = get_all_data()
    return data