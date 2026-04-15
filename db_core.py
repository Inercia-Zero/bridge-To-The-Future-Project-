import sqlite3
from datetime import datetime

DB_PATH = "mentoredu.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def _column_exists(cursor, table_name: str, column_name: str) -> bool:
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return any(col[1] == column_name for col in columns)

def init_db():
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL DEFAULT 'Nova conversa',
                subject TEXT NOT NULL DEFAULT 'Geral',
                owner_username TEXT NOT NULL DEFAULT 'global',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Migrações seguras
        if not _column_exists(cursor, "conversations", "subject"):
            cursor.execute("ALTER TABLE conversations ADD COLUMN subject TEXT NOT NULL DEFAULT 'Geral'")
        if not _column_exists(cursor, "conversations", "owner_username"):
            cursor.execute("ALTER TABLE conversations ADD COLUMN owner_username TEXT NOT NULL DEFAULT 'global'")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                image_path TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()

def init_materials_table():
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                teacher_name TEXT,
                content TEXT,
                file_name TEXT,
                file_path TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

# =========================================================
# CONVERSAS
# =========================================================

def ensure_default_conversation(subject: str, owner_username: str) -> int:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM conversations
            WHERE subject = ? AND owner_username = ?
            ORDER BY updated_at DESC LIMIT 1
        """, (subject, owner_username))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return create_new_conversation(subject, owner_username)
    finally:
        conn.close()

def create_new_conversation(subject: str, owner_username: str, title: str = "Nova conversa") -> int:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO conversations (title, subject, owner_username, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (title, subject, owner_username, now, now))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_active_conversation_id(subject: str, owner_username: str):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM conversations
            WHERE subject = ? AND owner_username = ?
            ORDER BY updated_at DESC LIMIT 1
        """, (subject, owner_username))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()

def list_conversations_by_mentor(subject: str, owner_username: str):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, subject, owner_username, created_at, updated_at
            FROM conversations
            WHERE subject = ? AND owner_username = ?
            ORDER BY updated_at DESC
        """, (subject, owner_username))
        rows = cursor.fetchall()
        return [
            {"id": r[0], "title": r[1], "subject": r[2], "owner_username": r[3], "created_at": r[4], "updated_at": r[5]}
            for r in rows
        ]
    finally:
        conn.close()

def renomear_conversa(conversation_id: int, novo_nome: str):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?", (novo_nome, now, conversation_id))
        conn.commit()
    finally:
        conn.close()

def deletar_conversa(conversation_id: int):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        conn.commit()
    finally:
        conn.close()

# =========================================================
# MENSAGENS
# =========================================================

def save_message(conversation_id: int, role: str, content: str, image_path: str | None = None):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO messages (conversation_id, role, content, image_path, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (conversation_id, role, content, image_path, now))
        cursor.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
        conn.commit()
    finally:
        conn.close()

def load_messages_for_conversation(conversation_id: int):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, content, image_path, created_at
            FROM messages WHERE conversation_id = ? ORDER BY id ASC
        """, (conversation_id,))
        rows = cursor.fetchall()
        return [{"role": r[0], "content": r[1], "image_path": r[2], "created_at": r[3]} for r in rows]
    finally:
        conn.close()

# =========================================================
# MATERIAIS
# =========================================================

def add_material(title, subject, teacher_name=None, content=None, file_name=None, file_path=None):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO materials (title, subject, teacher_name, content, file_name, file_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, subject, teacher_name, content, file_name, file_path, now))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def list_materials(limit: int = 10, subject: str | None = None):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        if subject:
            cursor.execute("SELECT * FROM materials WHERE subject = ? ORDER BY created_at DESC LIMIT ?", (subject, limit))
        else:
            cursor.execute("SELECT * FROM materials ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return [
            {"id": r[0], "title": r[1], "subject": r[2], "teacher_name": r[3], "content": r[4], 
             "file_name": r[5], "file_path": r[6], "created_at": r[7]}
            for r in rows
        ]
    finally:
        conn.close()
