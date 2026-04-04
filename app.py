import streamlit as st
from datetime import datetime

from db_core import (
    init_db,
    ensure_default_conversation,
    load_messages_for_conversation,
    save_message,
    list_conversations_by_mentor,
    create_new_conversation,
)

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Bridge to the Future",
    layout="wide",
)

# =========================================================
# LOGIN SIMPLES
# =========================================================
USERS = {
    "adenilson": "123",
    "orlando": "123",
    "francisco": "123",
}

def login(user, password):
    return USERS.get(user) == password


# =========================================================
# SESSION STATE
# =========================================================
if "logged" not in st.session_state:
    st.session_state.logged = False

if "user" not in st.session_state:
    st.session_state.user = None

if "current_mentor" not in st.session_state:
    st.session_state.current_mentor = "Matemática"


# =========================================================
# LOGIN SCREEN
# =========================================================
def render_login():

    st.markdown(
        """
        <div style="text-align:center; margin-top:80px;">
            <h1 style="font-size:3rem;">Bridge to the Future</h1>
            <p style="opacity:0.7;">
                Projeto educacional para docentes da rede pública
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if login(user, password):
                st.session_state.logged = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Acesso inválido")


# =========================================================
# MENTORES
# =========================================================
MASTERS = {
    "Matemática": {
        "desc": "Funções, álgebra e raciocínio lógico",
        "avatar": "assets/math.png",
    },
    "Física": {
        "desc": "Movimento, forças e energia",
        "avatar": "assets/physics.png",
    },
    "Metodologia Científica": {
        "desc": "Pesquisa, projetos e pensamento científico",
        "avatar": "assets/science.png",
    },
}


# =========================================================
# CHAT
# =========================================================
def render_chat():

    mentor = st.session_state.current_mentor
    user = st.session_state.user

    conv_id = ensure_default_conversation(mentor + "_" + user)

    messages = load_messages_for_conversation(conv_id)

    # HEADER LIMPO
    st.markdown(f"## {mentor}")
    st.caption(MASTERS[mentor]["desc"])

    st.markdown("---")

    # CHAT
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"**Você:** {msg['content']}")
        else:
            st.markdown(f"**Mestre:** {msg['content']}")

    # INPUT
    prompt = st.chat_input("Digite sua mensagem...")

    if prompt:

        save_message(conv_id, "user", prompt)

        resposta = gerar_resposta(prompt, mentor)

        save_message(conv_id, "assistant", resposta)

        st.rerun()


# =========================================================
# IA SIMPLES (placeholder)
# =========================================================
def gerar_resposta(prompt, mentor):

    return f"""
Estou te ajudando em {mentor}.

Pergunta:
{prompt}

(Resposta simulada — aqui entra sua API depois)
"""


# =========================================================
# SIDEBAR LIMPA
# =========================================================
def render_sidebar():

    st.sidebar.markdown("## Bridge to the Future")
    st.sidebar.markdown(f"👤 {st.session_state.user}")

    st.sidebar.markdown("---")

    for m in MASTERS.keys():
        if st.sidebar.button(m):
            st.session_state.current_mentor = m
            st.rerun()

    st.sidebar.markdown("---")

    if st.sidebar.button("Nova conversa"):
        create_new_conversation(st.session_state.current_mentor)
        st.rerun()


# =========================================================
# MAIN
# =========================================================
init_db()

if not st.session_state.logged:
    render_login()
else:
    render_sidebar()
    render_chat()
