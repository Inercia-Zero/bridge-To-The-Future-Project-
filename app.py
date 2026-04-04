import random
import streamlit as st

from theme import apply_theme
from prompts import build_prompt, is_smalltalk
from masters import MASTERS
from groq_client import ask_ai, ask_vision_ai
from db_core import (
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
from attachments import validate_upload, save_upload, extract_pdf_text
from graph_tools import maybe_generate_graph
from geometry_tools import maybe_generate_geometry_visual
from ui_components import render_message, render_landing_screen
from materials import render_materials_admin


# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Bridge to the Future",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()
init_db()
init_materials_table()

PROFESSOR_PASSWORD = "1234"  # troque depois


# =========================================================
# SESSION
# =========================================================
DEFAULTS = {
    "page": "welcome",   # welcome | masters | chat
    "user_role": "Aluno",
    "display_name": "",
    "professor_password_input": "",
    "professor_authenticated": False,
    "selected_area": None,
    "welcome_search_text": "",
    "current_conversation_id": None,
    "chat_history": [],
    "show_attach_panel": False,
    "show_materials_panel": False,
    "context_file_path": None,
    "context_file_name": None,
    "context_file_type": None,
    "context_text": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================
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


def go_to_welcome():
    st.session_state.page = "welcome"


def go_to_masters():
    st.session_state.page = "masters"


def open_area(area: str):
    st.session_state.selected_area = area
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


def open_conversation(conversation_id: int):
    st.session_state.current_conversation_id = conversation_id
    st.session_state.chat_history = load_messages_for_conversation(conversation_id)


def suggest_area_from_text(user_text: str):
    t = (user_text or "").strip().lower()

    if not t:
        return None

    if any(k in t for k in [
        "matemática", "matematica", "equação", "equacao", "função", "funcao",
        "bhaskara", "báscara", "álgebra", "algebra", "geometria",
        "trigonometria", "derivada", "integral", "logaritmo"
    ]):
        return "Matemática"

    if any(k in t for k in [
        "física", "fisica", "mru", "mruv", "força", "forca",
        "energia", "movimento", "velocidade", "aceleração", "aceleracao",
        "gravidade", "newton"
    ]):
        return "Física"

    if any(k in t for k in [
        "metodologia", "pesquisa", "artigo", "projeto científico",
        "projeto cientifico", "projeto", "projeto pessoal",
        "hipótese", "hipotese", "tema", "objetivo",
        "justificativa", "problema de pesquisa",
        "referencial", "iniciacao cientifica", "iniciação científica"
    ]):
        return "Metodologia Científica"

    if any(k in t for k in [
        "abnt", "relatório", "relatorio", "currículo", "curriculo",
        "resumo", "documento", "trabalho", "citação", "citacao",
        "referência", "referencia", "tcc"
    ]):
        return "Documentos Acadêmicos"

    return None


# =========================================================
# UI AUXILIAR
# =========================================================
def render_top_brand():
    st.markdown("## Bridge to the Future")
    st.caption("Projeto educacional para estudantes da rede pública.")


# =========================================================
# TELA 1 - ENTRADA
# =========================================================
def render_welcome_screen():
    st.markdown("<div style='max-width: 980px; margin: 0 auto;'>", unsafe_allow_html=True)

    render_top_brand()

    st.markdown("### Como você quer entrar hoje?")

    role = st.radio(
        "Perfil",
        ["Aluno", "Professor"],
        horizontal=True,
        key="welcome_role",
    )

    display_name = st.text_input(
        "Como você quer ser chamado?",
        value=st.session_state.display_name,
        key="welcome_display_name",
        placeholder="Ex: Iago, Mesquita, Professor Iago...",
    )

    password_ok = True

    if role == "Professor":
        password = st.text_input(
            "Senha do professor",
            type="password",
            key="welcome_prof_password",
            placeholder="Digite a senha",
        )
        password_ok = password == PROFESSOR_PASSWORD

        if password and not password_ok:
            st.error("Senha de professor incorreta.")

    st.markdown("---")
    st.markdown("### O que você está procurando hoje?")

    search_text = st.text_input(
        "Descreva sua necessidade",
        value=st.session_state.welcome_search_text,
        key="welcome_search_text",
        placeholder="Ex: Estou estudando função afim / Tenho dúvida em MRU / Preciso formatar em ABNT...",
    )

    suggested = suggest_area_from_text(search_text)
    if suggested:
        st.success(f"Sugestão automática: {suggested}")

    if st.button("Continuar", use_container_width=True):
        if not display_name.strip():
            st.warning("Digite como você quer ser chamado.")
            st.stop()

        if role == "Professor" and not password_ok:
            st.warning("Corrija a senha do professor para continuar.")
            st.stop()

        st.session_state.user_role = role
        st.session_state.display_name = display_name.strip()
        st.session_state.professor_authenticated = role == "Professor"
        st.session_state.selected_area = suggested
        st.session_state.page = "masters"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TELA 2 - ESCOLHA DOS MESTRES
# =========================================================
def render_masters_screen():
    st.markdown("<div style='max-width: 1120px; margin: 0 auto;'>", unsafe_allow_html=True)

    st.markdown(
        f"### Beleza, **{st.session_state.display_name}**. Agora escolha seu mestre."
    )

    if st.session_state.selected_area:
        st.info(f"Sugestão com base no que você escreveu: {st.session_state.selected_area}")

    render_landing_screen(MASTERS, open_area)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Voltar", use_container_width=True):
            st.session_state.page = "welcome"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TELA 3 - CHAT
# =========================================================
def render_chat_screen():
    area = st.session_state.selected_area

    if not area:
        st.session_state.page = "masters"
        st.rerun()
        return

    area_info = MASTERS[area]

    if st.session_state.current_conversation_id is None:
        cid = get_active_conversation_id(area) or ensure_default_conversation(area)
        st.session_state.current_conversation_id = cid
        st.session_state.chat_history = load_messages_for_conversation(cid)

    sidebar, main = st.columns([1.15, 4.2], gap="medium")

    with sidebar:
        st.markdown("### Bridge to the Future")
        st.caption(area_info.get("title", area))
        st.caption(f"Perfil: {st.session_state.user_role}")
        st.caption(f"Usuário: {st.session_state.display_name}")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Mestres", use_container_width=True):
                st.session_state.page = "masters"
                st.rerun()

        with c2:
            if st.button("Nova", use_container_width=True):
                new_id = create_new_conversation(area)
                st.session_state.current_conversation_id = new_id
                st.session_state.chat_history = []
                st.rerun()

        st.markdown("### Histórico")

        conversations = list_conversations_by_mentor(area)
        if not conversations:
            st.caption("Nenhuma conversa ainda.")
        else:
            for conv in conversations:
                active = conv
