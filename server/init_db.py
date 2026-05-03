import sqlite3
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_folder = os.path.join(base_dir, "database")
db_path = os.path.join(db_folder, "interviews.db")

os.makedirs(db_folder, exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    date TEXT NOT NULL,
    slot TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database and table created successfully.")
print("Database path:", db_path)
