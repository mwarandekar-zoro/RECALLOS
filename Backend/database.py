import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "recallos.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def create_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL UNIQUE,
            extension TEXT,
            size INTEGER,
            content TEXT,
            modified_at REAL
        )
    """)

    connection.commit()
    connection.close()


def save_file(file_info, content):
    connection = get_connection()

    connection.execute("""
        INSERT INTO files (
            name,
            path,
            extension,
            size,
            content,
            modified_at
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(path) DO UPDATE SET
            name = excluded.name,
            extension = excluded.extension,
            size = excluded.size,
            content = excluded.content,
            modified_at = excluded.modified_at
    """, (
        file_info["name"],
        file_info["path"],
        file_info["extension"],
        file_info["size"],
        content,
        file_info["modified_at"]
    ))

    connection.commit()
    connection.close()
    