import streamlit as st
import sqlite3
import random
from datetime import datetime
from prompts import build_prompt, is_smalltalk
from mentors import MENTORS
from groq import Groq

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="MentorEdu | Projeto Inércia Zero", layout="wide")

DB_PATH = "mentoredu.db"
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# DB
# =========================
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def listar_conversas():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM conversations ORDER BY updated_at DESC")
    data = cursor.fetchall()
    conn.close()
    return [{"id": d[0], "title": d[1]} for d in data]


def criar_conversa():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (title, created_at, updated_at) VALUES (?, ?, ?)",
        ("Nova conversa", datetime.now(), datetime.now()),
    )
    conn.commit()
    conv_id = cursor.lastrowid
    conn.close()
    return conv_id


def salvar_mensagem(conv_id, role, content):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
        (conv_id, role, content, datetime.now()),
    )
    conn.commit()
    conn.close()


def carregar_mensagens(conv_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id",
        (conv_id,),
    )
    data = cursor.fetchall()
    conn.close()
    return [{"role": d[0], "content": d[1]} for d in data]


# =========================
# NOVAS FUNÇÕES
# =========================

def deletar_conversa(conv_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
    cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    conn.close()


def renomear_conversa(conv_id, novo_nome):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
        (novo_nome, datetime.now(), conv_id),
    )
    conn.commit()
    conn.close()


# =========================
# SESSION
# =========================
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None

if "profile" not in st.session_state:
    st.session_state.profile = "Aluno"

# =========================
# SIDEBAR
# =========================
st.sidebar.image("logoifce.png", use_container_width=True)
st.sidebar.markdown("## MentorEdu")

# perfil
st.sidebar.radio(
    "Perfil",
    ["Aluno", "Professor"],
    key="profile"
)

# nova conversa
if st.sidebar.button("➕ Nova conversa"):
    st.session_state.current_conversation = criar_conversa()
    st.rerun()

st.sidebar.markdown("### Histórico")

conversas = listar_conversas()

for conv in conversas:
    col1, col2 = st.sidebar.columns([4, 1])

    with col1:
        if st.button(conv["title"], key=f"open_{conv['id']}"):
            st.session_state.current_conversation = conv["id"]

    with col2:
        if st.button("⋮", key=f"menu_{conv['id']}"):
            st.session_state[f"menu_{conv['id']}"] = not st.session_state.get(f"menu_{conv['id']}", False)

    if st.session_state.get(f"menu_{conv['id']}", False):
        new_name = st.sidebar.text_input("Renomear", key=f"rename_{conv['id']}")
        
        if st.sidebar.button("Salvar nome", key=f"save_{conv['id']}"):
            if new_name:
                renomear_conversa(conv["id"], new_name)
                st.rerun()

        if st.sidebar.button("🗑️ Apagar", key=f"del_{conv['id']}"):
            deletar_conversa(conv["id"])
            st.rerun()

# =========================
# MAIN
# =========================
st.title("Bridge to the Future")

mentor = st.selectbox("Escolha a área", list(MENTORS.keys()))

if st.session_state.current_conversation:
    mensagens = carregar_mensagens(st.session_state.current_conversation)

    for msg in mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Digite sua mensagem...")

    if user_input:
        salvar_mensagem(st.session_state.current_conversation, "user", user_input)

        with st.chat_message("user"):
            st.markdown(user_input)

        # SMALLTALK
        if is_smalltalk(user_input):
            resposta = random.choice([
                "E aí! Bora estudar o quê?",
                "Fala! O que você quer aprender hoje?",
                "Manda a dúvida 😄",
                "Bora! Qual é o desafio?",
                "Aqui não tem erro... só cálculo 😂"
            ])
        else:
            prompt = build_prompt(
                user_input=user_input,
                mentor=mentor,
                profile=st.session_state.profile,
                history=mensagens
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )

            resposta = response.choices[0].message.content

        salvar_mensagem(st.session_state.current_conversation, "assistant", resposta)

        with st.chat_message("assistant"):
            st.markdown(resposta)

else:
    st.info("Crie ou selecione uma conversa para começar.")
