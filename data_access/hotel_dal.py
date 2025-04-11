import os
import sqlite3
from typing import List, Tuple, Any

from app.model.hotel import Hotel
from app.util.db import fetch_all

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/hotel_reservation_sample.db")


def get_all_data() -> List[Tuple]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hotel")
    data = cursor.fetchall()
    conn.close()
    return data


def get_by_city(city: Tuple[str]) -> list[Any]:
    """
    Ruft alle Hotels in der gewünschten Stadt aus der Datenbank ab und mappt sie auf Hotel-Objekte.
    """
    query = "SELECT * FROM hotel AS H JOIN main.address A on H.address_id = A.address_id WHERE A.city = ?"

    data = fetch_all(query, city)

    return data
