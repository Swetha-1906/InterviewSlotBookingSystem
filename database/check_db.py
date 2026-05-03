import sqlite3

db_path = r"D:\6th sem\PP Project\InterviewSlotBookingSystem\database\interviews.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM appointments")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()