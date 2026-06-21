import sqlite3
from pathlib import Path

DB_PATH = Path("data/employee44.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EMPLOYEE (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Surname TEXT NOT NULL,
                ThirdName TEXT NOT NULL,
                Age INTEGER NOT NULL,
                Sex TEXT NOT NULL,
                DateAdm TEXT NOT NULL,
                Position TEXT NOT NULL,
                Department TEXT NOT NULL,
                PhoneNumber TEXT NOT NULL,
                EMail TEXT NOT NULL,
                Head TEXT NOT NULL,
                Photo TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ARCHIVE (
                id INTEGER,
                prichina TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        connection.commit()
