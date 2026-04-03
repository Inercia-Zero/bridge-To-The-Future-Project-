import sqlite3
from pathlib import Path

DB_PATH = Path("bridge_to_the_future.db")

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL DEFAULT 'Nova conversa',
            created_at TEXT,
            updated_at TEXT,
            mentor TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def init_materials_table() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            teacher_name TEXT,
            description TEXT,
            file_path TEXT,
            file_type TEXT,
            tags TEXT,
            uploaded_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def save_material_record(title, subject, teacher_name, description, file_path, file_type, tags, uploaded_at):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO materials (
            title, subject, teacher_name, description, file_path, file_type, tags, uploaded_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (title, subject, teacher_name, description, file_path, file_type, tags, uploaded_at),
    )
    conn.commit()
    conn.close()

def list_materials(limit=None):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = """
        SELECT id, title, subject, teacher_name, description, file_path, file_type, tags, uploaded_at
        FROM materials
        ORDER BY id DESC
    """
    if limit:
        query += f" LIMIT {int(limit)}"
    cur.execute(query)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
