import os
from typing import Tuple, Any
import sqlite3


def fetch_all(query: str, params: tuple = ()) -> list[Any]:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "../database/hotel_reservation_sample.db")
    """
    Führt eine SELECT-Query aus und gibt Spaltennamen + Zeilen zurück.
    """
    with  sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
    return data
