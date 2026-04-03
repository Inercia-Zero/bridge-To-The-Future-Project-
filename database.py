import sqlite3
from datetime import datetime

DB_PATH = "mentoredu.db"


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL DEFAULT 'Nova conversa',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    """)

    conn.commit()
    conn.close()


def listar_conversas():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, created_at, updated_at
        FROM conversations
        ORDER BY updated_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "created_at": row[2],
            "updated_at": row[3],
        }
        for row in rows
    ]


def criar_conversa(title="Nova conversa"):
    conn = get_conn()
    cursor = conn.cursor()

    agora = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO conversations (title, created_at, updated_at)
        VALUES (?, ?, ?)
    """, (title, agora, agora))

    conn.commit()
    conv_id = cursor.lastrowid
    conn.close()
    return conv_id


def salvar_mensagem(conversation_id, role, content):
    conn = get_conn()
    cursor = conn.cursor()

    agora = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO messages (conversation_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
    """, (conversation_id, role, content, agora))

    cursor.execute("""
        UPDATE conversations
        SET updated_at = ?
        WHERE id = ?
    """, (agora, conversation_id))

    conn.commit()
    conn.close()


def carregar_mensagens(conversation_id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
    """, (conversation_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "role": row[0],
            "content": row[1],
            "created_at": row[2],
        }
        for row in rows
    ]


def deletar_conversa(conversation_id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))

    conn.commit()
    conn.close()


def renomear_conversa(conversation_id, novo_nome):
    conn = get_conn()
    cursor = conn.cursor()

    agora = datetime.now().isoformat()

    cursor.execute("""
        UPDATE conversations
        SET title = ?, updated_at = ?
        WHERE id = ?
    """, (novo_nome, agora, conversation_id))

    conn.commit()
    conn.close()
