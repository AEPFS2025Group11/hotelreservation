import os
from typing import List

from app.model.address import Address

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/hotel_reservation_sample.db")


def get_all_addresses() -> List[Address]:
    pass
