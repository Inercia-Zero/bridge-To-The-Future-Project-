import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("bridge_to_the_future.db")

def now_iso():
    return datetime.utcnow().isoformat()

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mentor TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT 'Nova conversa',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            image_path TEXT,
            created_at TEXT NOT NULL
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

def create_new_conversation(mentor: str, title: str = "Nova conversa") -> int:
    conn = get_conn()
    cur = conn.cursor()
    ts = now_iso()
    cur.execute(
        """
        INSERT INTO conversations (mentor, title, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        """,
        (mentor, title, ts, ts),
    )
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid

def ensure_default_conversation(mentor: str) -> int:
    existing = get_active_conversation_id(mentor)
    if existing:
        return existing
    return create_new_conversation(mentor)

def get_active_conversation_id(mentor: str):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id FROM conversations
        WHERE mentor = ?
        ORDER BY updated_at DESC, id DESC
        LIMIT 1
        """,
        (mentor,),
    )
    row = cur.fetchone()
    conn.close()
    return row["id"] if row else None

def list_conversations_by_mentor(mentor: str):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, title, updated_at
        FROM conversations
        WHERE mentor = ?
        ORDER BY updated_at DESC, id DESC
        """,
        (mentor,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def load_messages_for_conversation(conversation_id: int):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT role, content, image_path
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def save_message(conversation_id: int, role: str, content: str, image_path=None):
    conn = get_conn()
    cur = conn.cursor()
    ts = now_iso()
    cur.execute(
        """
        INSERT INTO messages (conversation_id, role, content, image_path, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (conversation_id, role, content, image_path, ts),
    )
    cur.execute(
        """
        UPDATE conversations
        SET updated_at = ?
        WHERE id = ?
        """,
        (ts, conversation_id),
    )
    cur.execute(
        """
        SELECT COUNT(*) FROM messages
        WHERE conversation_id = ? AND role = 'user'
        """,
        (conversation_id,),
    )
    count = cur.fetchone()[0]
    if count == 1:
        title = " ".join(content.split())[:72] if content.strip() else "Nova conversa"
        cur.execute("UPDATE conversations SET title = ? WHERE id = ?", (title, conversation_id))
    conn.commit()
    conn.close()

def list_materials(limit=None, subject=None):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = """
        SELECT id, title, subject, teacher_name, description, file_path, file_type, tags, uploaded_at
        FROM materials
    """
    params = []
    if subject:
        query += " WHERE subject = ?"
        params.append(subject)
    query += " ORDER BY id DESC"
    if limit:
        query += f" LIMIT {int(limit)}"
    cur.execute(query, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

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
