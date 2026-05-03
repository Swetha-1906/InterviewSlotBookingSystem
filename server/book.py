#!C:/Python313/python.exe

import cgi
import sqlite3

print("Content-Type: text/html\n")

form = cgi.FieldStorage()

name = form.getvalue("name")
email = form.getvalue("email")
date = form.getvalue("date")
slot = form.getvalue("slot")

conn = sqlite3.connect("../database/interviews.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM appointments WHERE date=? AND slot=?", (date, slot))
existing = cursor.fetchone()

if existing:
    print("<h3>Slot already booked. Please choose another slot.</h3>")
else:
    cursor.execute(
        "INSERT INTO appointments (name, email, date, slot) VALUES (?, ?, ?, ?)",
        (name, email, date, slot)
    )
    conn.commit()
    print("<h3>Booking Confirmed Successfully!</h3>")

conn.close()