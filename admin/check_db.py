import sqlite3

conn = sqlite3.connect(r"D:\6th sem\PP Project\InterviewSlotBookingSystem\database\interviews.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM appointments")
rows = cursor.fetchall()

print("\n--- Booked Slots ---\n")
for row in rows:
    print(row)

conn.close()