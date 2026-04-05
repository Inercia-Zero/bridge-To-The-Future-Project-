import random
from pathlib import Path
from html import escape

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
from ui_components import render_landing_screen
from materials import render_materials_admin


# =========================================================
# CONFIG
# =========================================================
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
# ACESSOS
# =========================================================
USERS = {
    "adenilson": "1234",
    "orlando": "1234",
    "francisco": "1234",
    "mesquita": "1234",
}


# =========================================================
# SESSION
# =========================================================
DEFAULTS = {
    "page": "welcome",   # welcome | masters | chat
    "logged": False,
    "display_name": "",
    "selected_area": None,
    "welcome_search_text": "",
    "current_conversation_id": None,
    "chat_history": [],
    "show_materials_panel": False,
    "context_file_path": None,
    "context_file_name": None,
    "context_file_type": None,
    "context_text": None,
    "chat_input_key": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================
def get_owner() -> str:
    return (st.session_state.get("display_name") or "").strip().lower()


def pretty_name(name: str) -> str:
    if not name:
        return ""
    parts = str(name).strip().split()
    return " ".join(p[:1].upper() + p[1:].lower() for p in parts if p)


def greeting_reply():
    respostas = [
        "E aí! Bora planejar algo bom?",
        "Fala! O que você quer montar hoje?",
        "Manda a ideia 😄",
        "Bora! Qual conteúdo?",
        "Pode mandar 👊",
    ]
    return random.choice(respostas)


def login_ok(username: str, password: str) -> bool:
    return USERS.get((username or "").strip().lower()) == password


def clear_active_context():
    st.session_state.context_file_path = None
    st.session_state.context_file_name = None
    st.session_state.context_file_type = None
    st.session_state.context_text = None


def reset_chat_input():
    st.session_state.chat_input_key += 1


def go_to_welcome():
    st.session_state.page = "welcome"
    st.rerun()


def go_to_masters():
    st.session_state.page = "masters"
    st.rerun()


def open_area(area: str):
    owner = get_owner()

    st.session_state.selected_area = area
    st.session_state.page = "chat"

    cid = ensure_default_conversation(area, owner)
    st.session_state.current_conversation_id = cid
    st.session_state.chat_history = load_messages_for_conversation(cid)

    st.session_state.show_materials_panel = False
    clear_active_context()
    reset_chat_input()
    st.rerun()


def open_conversation(conversation_id: int):
    st.session_state.current_conversation_id = conversation_id
    st.session_state.chat_history = load_messages_for_conversation(conversation_id)
    reset_chat_input()
    st.rerun()


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
        "gravidade", "newton", "projétil", "projetil"
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


def render_top_brand():
    st.markdown(
        """
        <div style="text-align:center; margin-top: 24px; margin-bottom: 6px;">
            <div style="font-size: 2.6rem; font-weight: 900;">Bridge to the Future</div>
            <div style="opacity: 0.75; margin-top: 6px;">
                Projeto educacional para docentes da rede pública
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def normalize_chat_submission(submission):
    """
    st.chat_input:
    - sem accept_file => str | None
    - com accept_file => objeto com .text e .files
    """
    if submission is None:
        return "", []

    if isinstance(submission, str):
        return submission, []

    text = ""
    files = []

    if hasattr(submission, "text"):
        text = submission.text or ""
    elif isinstance(submission, dict):
        text = submission.get("text", "") or ""

    if hasattr(submission, "files"):
        files = submission.files or []
    elif isinstance(submission, dict):
        files = submission.get("files", []) or []

    return text, files


def should_use_vision(user_text: str, image_paths: list[str]) -> bool:
    """
    A imagem NÃO deve ser usada em toda pergunta automaticamente.
    Só usa visão quando:
    - há imagem e o professor pede análise visual
    - ou só enviou imagem sem texto
    """
    if not image_paths:
        return False

    t = (user_text or "").strip().lower()

    if not t:
        return True

    vision_keywords = [
        "imagem", "foto", "figura", "gráfico", "grafico", "observe",
        "veja", "analise", "analisa", "analisar", "descreva",
        "o que tem", "nessa imagem", "nesta imagem", "na imagem",
        "print", "captura", "diagrama", "quadro", "tabela", "esquema"
    ]
    return any(k in t for k in vision_keywords)


def process_uploaded_files(uploaded_files):
    """
    Regras:
    - PDF/TXT => viram contexto ativo persistente
    - Imagem => NÃO vira contexto global automaticamente
    - A imagem fica na mensagem do chat
    """
    attached_labels = []
    image_paths = []
    saved_items = []

    for uploaded in uploaded_files:
        error = validate_upload(uploaded)
        if error:
            raise ValueError(error)

        file_path, file_name, file_type = save_upload(uploaded)
        saved_items.append((file_path, file_name, file_type))

        if file_type == "pdf":
            attached_labels.append(f"📄 PDF: {file_name}")
        elif file_type == "text":
            attached_labels.append(f"📝 Texto: {file_name}")
        elif file_type == "image":
            image_paths.append(file_path)
        else:
            attached_labels.append(f"📎 Arquivo: {file_name}")

    # último PDF/TXT enviado vira contexto
    last_context_item = None
    for file_path, file_name, file_type in reversed(saved_items):
        if file_type in ("pdf", "text"):
            last_context_item = (file_path, file_name, file_type)
            break

    if last_context_item:
        file_path, file_name, file_type = last_context_item
        st.session_state.context_file_path = file_path
        st.session_state.context_file_name = file_name
        st.session_state.context_file_type = file_type

        if file_type == "pdf":
            st.session_state.context_text = extract_pdf_text(file_path)
        elif file_type == "text":
            with open(file_path, "r", encoding="utf-8") as f:
                st.session_state.context_text = f.read()

    return {
        "attached_labels": attached_labels,
        "image_paths": image_paths,
    }


def render_chat_css():
    st.markdown(
        """
        <style>
        .sticky-chat-header {
            position: sticky;
            top: 0.35rem;
            z-index: 20;
            background: rgba(23, 23, 23, 0.92);
            backdrop-filter: blur(10px);
            border: 1px solid #2a2a2a;
            border-radius: 18px;
            padding: 16px 18px 14px 18px;
            margin-bottom: 14px;
        }

        .sticky-chat-title {
            text-align: center;
            font-size: 1.5rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            color: #f5f5f5;
            margin: 0;
            line-height: 1.15;
        }

        .sticky-chat-subtitle {
            text-align: center;
            font-size: 1rem;
            font-weight: 700;
            color: #cfcfcf;
            margin-top: 8px;
        }

        .chat-stream-wrap {
            max-width: 920px;
            margin: 0 auto;
            padding-bottom: 0.5rem;
        }

        .chat-row {
            display: flex;
            width: 100%;
            margin-bottom: 14px;
        }

        .chat-row.user {
            justify-content: flex-start;
        }

        .chat-row.assistant {
            justify-content: flex-end;
        }

        .chat-bubble {
            width: fit-content;
            max-width: 78%;
            padding: 14px 16px;
            border-radius: 18px;
            border: 1px solid #2a2a2a;
            line-height: 1.7;
            font-size: 0.98rem;
            box-shadow: 0 8px 18px rgba(0,0,0,0.16);
            word-break: break-word;
            white-space: pre-wrap;
        }

        .chat-row.user .chat-bubble {
            background: #202020;
            color: #f5f5f5;
            border-top-left-radius: 6px;
        }

        .chat-row.assistant .chat-bubble {
            background: #2a2a2a;
            color: #f5f5f5;
            border-top-right-radius: 6px;
        }

        .chat-attachments {
            max-width: 78%;
            margin-top: -6px;
            margin-bottom: 12px;
            font-size: 0.86rem;
            color: #b8b8b8;
        }

        .chat-row.user + .chat-attachments {
            text-align: left;
        }

        .context-inline {
            max-width: 920px;
            margin: 0 auto 12px auto;
        }

        @media (max-width: 768px) {
            .chat-bubble,
            .chat-attachments {
                max-width: 92%;
            }

            .sticky-chat-title {
                font-size: 1.22rem;
            }

            .sticky-chat-subtitle {
                font-size: 0.92rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_chat_bubble(role: str, content: str):
    if not content:
        return

    safe = escape(content)
    row_class = "user" if role == "user" else "assistant"

    st.markdown(
        f"""
        <div class="chat-row {row_class}">
            <div class="chat-bubble">{safe}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_item(item: dict):
    role = item.get("role", "assistant")
    content = (item.get("content") or "").strip()
    image_path = item.get("image_path")
    attachment_labels = item.get("attachment_labels", [])

    if content:
        render_chat_bubble(role, content)

    if image_path and Path(image_path).exists():
        row_class = "user" if role == "user" else "assistant"
        with st.container():
            st.markdown(f'<div class="chat-row {row_class}">', unsafe_allow_html=True)
            st.image(image_path, use_container_width=False, width=360)
            st.markdown("</div>", unsafe_allow_html=True)

    if attachment_labels:
        text = "<br>".join(escape(x) for x in attachment_labels)
        row_class = "user" if role == "user" else "assistant"
        align = "left" if role == "user" else "right"
        st.markdown(
            f"""
            <div class="chat-row {row_class}">
                <div class="chat-attachments" style="text-align:{align};">
                    {text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# TELA 1 - ACESSO
# =========================================================
def render_welcome_screen():
    st.markdown("<div style='max-width: 980px; margin: 0 auto;'>", unsafe_allow_html=True)

    render_top_brand()

    st.markdown("### Acesso")

    username = st.text_input(
        "Professor",
        value=st.session_state.display_name,
        key="welcome_username",
        placeholder="Digite seu nome de acesso",
    )

    password = st.text_input(
        "Senha",
        type="password",
        key="welcome_password",
        placeholder="Digite sua senha",
    )

    st.markdown("---")
    st.markdown("### O que você está procurando hoje?")

    search_text = st.text_input(
        "Descreva sua necessidade",
        value=st.session_state.welcome_search_text,
        key="welcome_search_text",
        placeholder="Ex: Gerar questões sobre MRU / Planejar aula sobre função afim / Formatar material em ABNT...",
    )

    suggested = suggest_area_from_text(search_text)
    if suggested:
        st.success(f"Sugestão automática: {suggested}")

    if st.button("Entrar", use_container_width=True):
        if not username.strip():
            st.warning("Digite seu nome de acesso.")
            st.stop()

        if not password.strip():
            st.warning("Digite sua senha.")
            st.stop()

        if not login_ok(username, password):
            st.error("Professor ou senha inválidos.")
            st.stop()

        st.session_state.logged = True
        st.session_state.display_name = username.strip().lower()
        st.session_state.selected_area = suggested
        go_to_masters()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TELA 2 - ESCOLHA DOS MESTRES
# =========================================================
def render_masters_screen():
    st.markdown("<div style='max-width: 1120px; margin: 0 auto;'>", unsafe_allow_html=True)

    st.markdown(
        f"### Bem-vindo, **Professor {pretty_name(st.session_state.display_name)}**. Escolha seu mestre."
    )

    if st.session_state.selected_area:
        st.info(f"Sugestão com base no que você escreveu: {st.session_state.selected_area}")

    render_landing_screen(MASTERS, open_area)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Sair", use_container_width=True):
            st.session_state.logged = False
            st.session_state.display_name = ""
            st.session_state.selected_area = None
            st.session_state.current_conversation_id = None
            st.session_state.chat_history = []
            st.session_state.show_materials_panel = False
            clear_active_context()
            reset_chat_input()
            go_to_welcome()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TELA 3 - CHAT
# =========================================================
def render_chat_screen():
    area = st.session_state.selected_area
    owner = get_owner()
    owner_pretty = pretty_name(owner)

    if not area:
        go_to_masters()
        return

    area_info = MASTERS.get(area, {"title": area, "description": ""})
    mentor_title = area_info.get("title", area)

    if st.session_state.current_conversation_id is None:
        cid = get_active_conversation_id(area, owner) or ensure_default_conversation(area, owner)
        st.session_state.current_conversation_id = cid
        st.session_state.chat_history = load_messages_for_conversation(cid)

    # SIDEBAR NATIVA E ENCOLHÍVEL
    with st.sidebar:
        st.markdown("## Bridge to the Future")
        st.caption(area_info.get("title", area))
        st.caption(f"Professor: {owner_pretty
