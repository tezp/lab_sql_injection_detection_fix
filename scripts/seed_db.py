import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / "app" / "globomantics.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

users = [
    ("alice", "password123", "employee"),
    ("bob", "builder456", "employee"),
    ("admin", "globoadmin!", "administrator")
]

cursor.executemany(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    users
)

connection.commit()
connection.close()

print("[+] Database seeded successfully.")