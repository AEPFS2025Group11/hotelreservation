import sqlite3

conn = sqlite3.connect("./database/hotel_reservation_sample.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM address")
print(cursor.fetchall())
