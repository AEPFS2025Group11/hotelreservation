import os
from typing import List, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/hotel_reservation_sample.db")


def get_all_data() -> List[Tuple]:
    pass
