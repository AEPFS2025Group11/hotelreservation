import sqlite3
import os
from typing import List

from app.model.address import Address
from app.util.mapper import map_row_to_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/hotel_reservation_sample.db")


def get_all_addresses() -> List[Address]:
    """
    Ruft alle Adressen aus der Datenbank ab und mappt sie auf Address-Objekte.
    """
    query = "SELECT * FROM Address"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

    return [map_row_to_model(row, column_names, Address) for row in rows]
