import os
import random
import streamlit as st

from theme import apply_theme
from mentors import MENTORS
from database import (
    init_db,
    init_materials_table,
    ensure_default_conversation,
    get_active_conversation_id,
    list_conversations_by_mentor,
    load_messages_for_conversation,
    save_message,
    create_new_conversation,
    list_materials,
)
from prompts import build_prompt, is_smalltalk
from groq_client import ask_ai, ask_vision_ai
from ui_components import render_message
from materials import render_materials_admin
from attachments import validate_upload, save_upload, extract_pdf_text
from graph_tools import maybe_generate_graph
from geometry_tools import maybe_generate_geometry_visual


st.set_page_config(
    page_title="Bridge to the Future",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_db()
init_materials_table()

# =========================================================
# SESSION STATE
# =========================================================
DEFAULTS = {
    "page": "home",  # home | chat
    "selected_area": None,
    "profile": "Aluno",
    "current_conversation_id": None,
    "chat_history": [],
    "show_materials_panel": False,
    "show_attach_panel": False,
    "context_file_path": None,
    "context_file_name": None,
    "context_file_type": None,
    "context_text": None,
    "last_graph_context": {
        "mode": None,
        "function": None,
        "points": None,
        "linked": False,
        "area": None,
    },
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================
def open_area(area: str, profile: str):
    st.session_state.selected_area = area
    st.session_state.profile = profile
    st.session_state.page = "chat"

    cid = ensure_default_conversation(area)
    st.session_state.current_conversation_id = cid
    st.session_state.chat_history = load_messages_for_conversation(cid)

    st.session_state.show_attach_panel = False
    st.session_state.show_materials_panel = False
    st.session_state.context_file_path = None
    st.session_state.context_file_name = None
    st.session_state.context_file_type = None
    st.session_state.context_text = None

    st.session_state.last_graph_context = {
        "mode": None,
        "function": None,
        "points": None,
        "linked": False,
        "area": area,
    }

    st.rerun()


def go_home():
    st.session_state.page = "home"
    st.session_state.selected_area = None
    st.session_state.current_conversation_id = None
    st.session_state.chat_history = []
    st.session_state.show_attach_panel = False
    st.session_state.show_materials_panel = False
    st.session_state.context_file_path = None
    st.session_state.context_file_name = None
    st.session_state.context_file_type = None
    st.session_state.context_text = None
    st.rerun()


def open_conversation(conversation_id: int):
    st.session_state.current_conversation_id = conversation_id
    st.session_state.chat_history = load_messages_for_conversation(conversation_id)
    st.rerun()


def greeting_reply():
    respostas = [
        "E aí! Bora estudar o quê?",
        "Fala! O que você quer aprender hoje?",
        "Manda a dúvida 😄",
        "Bora! Qual é o desafio?",
        "Pode perguntar sem medo 👊",
        "Aqui não tem erro... só cálculo 😂",
    ]
    return random.choice(respostas)


def render_logo_project_block():
    col1, col2 = st.columns([1.1, 4.3], gap="medium")

    with col1:
        if os.path.exists("logoifce.png"):
            st.image("logoifce.png", width=120)

    with col2:
        if os.path.exists("logoprojeto.png"):
            st.image("logoprojeto.png", width=240)

    st.markdown("## Bridge to the Future")
    st.caption("Projeto educacional para estudantes da rede pública.")


def render_home():
    st.markdown("<div style='max-width: 1050px; margin: 0 auto;'>", unsafe_allow_html=True)

    render_logo_project_block()

    st.markdown("### Escolha sua área de estudo")

    areas = list(MENTORS.keys())
