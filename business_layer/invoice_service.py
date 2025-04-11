from app.data_access_layer.invoice_dal import *

def get_all():
    data = get_all_data()
    return data