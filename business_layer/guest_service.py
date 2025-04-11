from app.data_access_layer.guest_dal import *

def get_all():
    data = get_all_data()
    return data