import random
import sqlite3

import streamlit as st
import db_core as db_module

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
)
from attachments import validate_upload, save_upload, extract_pdf_text
from graph_tools import maybe_generate_graph
from geometry_tools import maybe_generate_geometry_visual
from ui_components import render_message, render_landing_screen


# =========================================================
# CONFIG
# =========================================================
PROJECT_TITLE = "Bridge to the Future Project"
PROJECT_SUBTITLE = "Projeto do PIBID voltado ao apoio docente com IA"

st.set_page_config(
    page_title=PROJECT_TITLE,
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
    "Adenilson": "1234",
    "Orlando": "1234",
    "Mesquita": "1234",
    "Francisco": "1234",
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
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================
def normalize_username(username: str) -> str:
    return (username or "").strip().lower()


def resolve_username(username: str) -> str | None:
    normalized = normalize_username(username)
    for display_name in USERS.keys():
        if display_name.lower() == normalized:
            return display_name
    return None


def get_owner() -> str:
    return normalize_username(st.session_state.get("display_name") or "")


def get_owner_display() -> str:
    owner = (st.session_state.get("display_name") or "").strip()
    return owner or "Professor"


def greeting_reply():
    respostas = [
        "E aí! Bora planejar o que hoje?",
        "Fala! O que você quer montar hoje?",
        "Fala Mestre, Manda a ideia 😄",
        "Bora! Qual conteúdo?",
        "Cuida,pode mandar 10! 👊",
        "Qual a dúvida, Mestre?🫡",
        "Em que posso ser útil hoje?",
        "Como posso te salvar hoje?",
        "Qual o B.O. de hoje?",
        "Bora! Me deixa ser útilno que hoje",
        "E aí, mestre! Quer ajuda em quê?",
        "Fala, Professor! Qual a bomba do dia?",
        "Como vai a vida docente, Mestre?",
        
        
    
    ]
    return random.choice(respostas)


def login_ok(username: str, password: str) -> bool:
    canonical_name = resolve_username(username)
    if not canonical_name:
        return False
    return USERS.get(canonical_name) == password


def canonical_username(username: str) -> str:
    return resolve_username(username) or (username or "").strip().title()


def get_db_path() -> str:
    for attr in ("DB_PATH", "db_path", "DATABASE_PATH"):
        value = getattr(db_module, attr, None)
        if value:
            return str(value)
    return "mentoredu.db"


def rename_conversation_persistent(conversation_id: int, new_title: str) -> tuple[bool, str]:
    title = (new_title or "").strip()
    if not title:
        return False, "Digite um novo título."

    try:
        with sqlite3.connect(get_db_path()) as conn:
            conn.execute(
                """
                UPDATE conversations
                SET title = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (title, conversation_id),
            )
            conn.commit()
        return True, "Conversa renomeada."
    except Exception as e:
        return False, f"Não foi possível renomear: {e}"


def delete_conversation_persistent(conversation_id: int) -> tuple[bool, str]:
    try:
        with sqlite3.connect(get_db_path()) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            conn.commit()
        return True, "Conversa excluída."
    except Exception as e:
        return False, f"Não foi possível excluir: {e}"


def go_to_welcome():
    st.session_state.page = "welcome"
    st.rerun()


def go_to_masters():
    st.session_state.page = "masters"
    st.rerun()


def render_global_footer():
    st.markdown(
        """
        <div class="app-footer-fixed">
            <span>Bridge to the Future Project</span>
            <span class="app-footer-sep">•</span>
            <span>Desenvolvido por Iago Mesquita</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def open_area(area: str):
    owner = get_owner()

    st.session_state.selected_area = area
    st.session_state.page = "chat"

    cid = ensure_default_conversation(area, owner)
    st.session_state.current_conversation_id = cid
    st.session_state.chat_history = load_messages_for_conversation(cid)

    st.rerun()


def open_conversation(conversation_id: int):
    st.session_state.current_conversation_id = conversation_id
    st.session_state.chat_history = load_messages_for_conversation(conversation_id)
    st.rerun()


def open_fallback_conversation(area: str, owner: str):
    remaining = list_conversations_by_mentor(area, owner)
    if remaining:
        new_id = remaining[0]["id"]
    else:
        new_id = ensure_default_conversation(area, owner)

    st.session_state.current_conversation_id = new_id
    st.session_state.chat_history = load_messages_for_conversation(new_id)


def suggest_area_from_text(user_text: str):
    t = (user_text or "").strip().lower()

    if not t:
        return None

    if any(k in t for k in [
        "matemática", "matematica", "equação", "equacao", "função", "funcao",
        "bhaskara", "báscara", "álgebra", "algebra", "geometria",
        "trigonometria", "derivada", "integral", "logaritmo", "Adenilson"
    ]):
        return "Matemática"

    if any(k in t for k in [
        "física", "fisica", "mru", "mruv", "força", "forca",
        "energia", "movimento", "velocidade", "aceleração", "aceleracao",
        "gravidade", "newton", "projétil", "projetil", "Orlando"
    ]):
        return "Física"

    if any(k in t for k in [
        "metodologia", "pesquisa", "artigo", "projeto científico",
        "projeto cientifico", "projeto", "projeto pessoal",
        "hipótese", "hipotese", "tema", "objetivo",
        "justificativa", "problema de pesquisa",
        "referencial", "iniciacao cientifica", "iniciação científica","Francisco"
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
        f"""
        <div class="welcome-brand">
            <div class="welcome-brand-title">{PROJECT_TITLE}</div>
            <div class="welcome-brand-subtitle">{PROJECT_SUBTITLE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def should_use_vision(user_text: str, image_paths: list[str]) -> bool:
    if not image_paths:
        return False

    t = (user_text or "").strip().lower()

    if not t:
        return True

    vision_keywords = [
        "imagem", "foto", "figura", "gráfico", "grafico", "observe",
        "veja", "analise", "analisa", "analisar", "descreva",
        "o que tem", "nessa imagem", "nesta imagem", "na imagem",
        "print", "captura", "diagrama"
    ]
    return any(k in t for k in vision_keywords)


def build_file_badge(file_name: str, file_type: str) -> str:
    label = file_type.upper() if file_type else "ARQUIVO"
    return f"📎 {label}: {file_name}"


def process_uploaded_files(uploaded_files):
    """
    Regras do chat:
    - imagem/pdf/txt entram como anexos da mensagem atual
    - não viram contexto global da conversa
    - PDF/TXT geram contexto transitório só para esta resposta
    """
    attached_labels = []
    image_paths = []
    saved_items = []

    transient_context_text = None
    transient_context_file_name = None
    transient_context_file_type = None

    if not uploaded_files:
        return {
            "attached_labels": attached_labels,
            "image_paths": image_paths,
            "saved_items": saved_items,
            "transient_context_text": transient_context_text,
            "transient_context_file_name": transient_context_file_name,
            "transient_context_file_type": transient_context_file_type,
        }

    for uploaded in uploaded_files:
        error = validate_upload(uploaded)
        if error:
            raise ValueError(error)

        file_path, file_name, file_type = save_upload(uploaded)
        saved_items.append((file_path, file_name, file_type))
        attached_labels.append(build_file_badge(file_name, file_type))

        if file_type == "image":
            image_paths.append(file_path)

        if file_type == "pdf":
            transient_context_text = extract_pdf_text(file_path)
            transient_context_file_name = file_name
            transient_context_file_type = file_type
        elif file_type == "text":
            with open(file_path, "r", encoding="utf-8") as f:
                transient_context_text = f.read()
            transient_context_file_name = file_name
            transient_context_file_type = file_type

    return {
        "attached_labels": attached_labels,
        "image_paths": image_paths,
        "saved_items": saved_items,
        "transient_context_text": transient_context_text,
        "transient_context_file_name": transient_context_file_name,
        "transient_context_file_type": transient_context_file_type,
    }


def normalize_chat_submission(submission):
    """
    st.chat_input:
    - sem accept_file => retorna string ou None
    - com accept_file => retorna objeto dict-like com .text e .files
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


def render_chat_item(item: dict):
    render_message(item)


# =========================================================
# TELA 1 - ACESSO
# =========================================================
def render_welcome_screen():
    st.markdown("<div style='max-width: 980px; margin: 0 auto;'>", unsafe_allow_html=True)

    render_top_brand()

    st.markdown("### Acesso")

    username = st.text_input(
        "Usuário",
        key="welcome_username",
        placeholder="Ex: Mesquita, Orlando, Adenilson...",
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
        key="welcome_search_text",
        placeholder="Ex: Gerar questões sobre MRU / Planejar aula sobre função afim / Formatar material em ABNT...",
    )

    suggested = suggest_area_from_text(search_text) if (search_text or "").strip() else None
    if suggested:
        st.success(f"Sugestão automática: {suggested}")

    if st.button("Entrar", use_container_width=True):
        if not username.strip():
            st.warning("Digite seu usuário.")
            st.stop()

        if not password.strip():
            st.warning("Digite sua senha.")
            st.stop()

        if not login_ok(username, password):
            st.error("Usuário ou senha inválidos.")
            st.stop()

        st.session_state.logged = True
        st.session_state.display_name = canonical_username(username)
        st.session_state.selected_area = suggested if (search_text or "").strip() else None
        go_to_masters()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TELA 2 - ESCOLHA DOS MESTRES
# =========================================================
def render_masters_screen():
    st.markdown("<div style='max-width: 1120px; margin: 0 auto;'>", unsafe_allow_html=True)

    st.markdown(
        f"### Bem-vindo, **{get_owner_display()}**. Escolha seu mestre."
    )

    if st.session_state.selected_area:
        st.info(f"Sugestão com base no que você escreveu: {st.session_state.selected_area}")

    render_landing_screen(MASTERS, open_area)

    c1, _ = st.columns([1, 1])

    with c1:
        if st.button("Sair", use_container_width=True):
            st.session_state.logged = False
            st.session_state.display_name = ""
            st.session_state.selected_area = None
            st.session_state.current_conversation_id = None
            st.session_state.chat_history = []
            st.session_state.welcome_search_text = ""
            st.session_state.welcome_username = ""
            st.session_state.welcome_password = ""
            go_to_welcome()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TELA 3 - CHAT
# =========================================================
def render_chat_screen():
    area = st.session_state.selected_area
    owner = get_owner()
    owner_display = get_owner_display()

    if not area:
        go_to_masters()
        return

    area_info = MASTERS.get(area, {"title": area, "description": ""})

    if st.session_state.current_conversation_id is None:
        cid = get_active_conversation_id(area, owner) or ensure_default_conversation(area, owner)
        st.session_state.current_conversation_id = cid
        st.session_state.chat_history = load_messages_for_conversation(cid)

    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <div class="sidebar-brand-kicker">{PROJECT_TITLE}</div>
                <div class="sidebar-brand-title">{area_info.get("title", area)}</div>
                <div class="sidebar-brand-user">Professor {owner_display}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Mestres", use_container_width=True):
                go_to_masters()

        with c2:
            if st.button("Nova", use_container_width=True):
                new_id = create_new_conversation(area, owner)
                st.session_state.current_conversation_id = new_id
                st.session_state.chat_history = []
                st.rerun()

        st.markdown("### Histórico")

        conversations = list_conversations_by_mentor(area, owner)
        if not conversations:
            st.caption("Nenhuma conversa ainda.")
        else:
            for conv in conversations:
                conv_id = conv["id"]
                conv_title = conv["title"]
                conv_updated = str(conv["updated_at"])[:16].replace("T", " ")
                active = conv_id == st.session_state.current_conversation_id

                left, right = st.columns([0.82, 0.18], gap="small")

                with left:
                    label = ("● " if active else "") + str(conv_title)
                    if st.button(
                        label,
                        key=f"open_conv_{conv_id}",
                        use_container_width=True,
                    ):
                        open_conversation(conv_id)

                    st.caption(conv_updated)

                with right:
                    with st.popover("⋮", key=f"menu_{conv_id}", width="content"):
                        new_title = st.text_input(
                            "Novo título",
                            value=str(conv_title),
                            key=f"rename_input_{conv_id}",
                        )

                        if st.button("Renomear", key=f"rename_btn_{conv_id}", use_container_width=True):
                            ok, message = rename_conversation_persistent(conv_id, new_title)
                            if ok:
                                if conv_id == st.session_state.current_conversation_id:
                                    st.session_state.chat_history = load_messages_for_conversation(conv_id)
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

                        if st.button("Excluir conversa", key=f"delete_btn_{conv_id}", use_container_width=True):
                            ok, message = delete_conversation_persistent(conv_id)
                            if ok:
                                if conv_id == st.session_state.current_conversation_id:
                                    open_fallback_conversation(area, owner)
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

                st.markdown("<div class='history-divider'></div>", unsafe_allow_html=True)

    st.markdown('<div class="chat-main-wrap">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="chat-topbar">
            <div class="chat-topbar-kicker">{PROJECT_TITLE}</div>
            <div class="chat-topbar-title">{area_info.get("title", area)}</div>
            <div class="chat-topbar-meta">Professor {owner_display}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for item in st.session_state.chat_history:
        render_chat_item(item)

    st.markdown("</div>", unsafe_allow_html=True)

    submission = st.chat_input(
        f"Converse com o mestre de {area.lower()}...",
        key="main_chat_input",
        accept_file="multiple",
        file_type=["pdf", "png", "jpg", "jpeg", "webp", "txt"],
        max_upload_size=25,
    )

    user_input, uploaded_files = normalize_chat_submission(submission)

    if submission is not None:
        if not (user_input or "").strip() and not uploaded_files:
            st.stop()

        cid = st.session_state.current_conversation_id

        attached_labels = []
        image_paths = []
        transient_context_text = None
        transient_context_file_name = None
        transient_context_file_type = None

        if uploaded_files:
            try:
                processed = process_uploaded_files(uploaded_files)
                attached_labels = processed["attached_labels"]
                image_paths = processed["image_paths"]
                transient_context_text = processed["transient_context_text"]
                transient_context_file_name = processed["transient_context_file_name"]
                transient_context_file_type = processed["transient_context_file_type"]
            except Exception as e:
                st.error(f"Erro ao processar arquivo: {e}")
                st.stop()

        clean_text = (user_input or "").strip()

        non_image_attachment_labels = [
            label for label in attached_labels
            if not label.lower().startswith("📎 image")
        ]

        user_item = {
            "role": "user",
            "content": clean_text,
            "image_path": image_paths[0] if image_paths else None,
            "attachment_labels": non_image_attachment_labels,
        }

        st.session_state.chat_history.append(user_item)
        save_message(
            cid,
            "user",
            clean_text,
            image_path=image_paths[0] if image_paths else None,
        )

        graph_path = None
        graph_meta = {}

        if clean_text:
            try:
                graph_result = maybe_generate_graph(clean_text, area)
                if graph_result is not None and isinstance(graph_result, tuple) and len(graph_result) == 2:
                    graph_path, graph_meta = graph_result
            except Exception as e:
                graph_path, graph_meta = None, {}
                print("Erro ao gerar gráfico:", e)

        geometry_path = None
        geometry_caption = None

        if clean_text:
            try:
                geometry_result = maybe_generate_geometry_visual(clean_text, area)
                if geometry_result is not None and isinstance(geometry_result, tuple) and len(geometry_result) == 2:
                    geometry_path, geometry_caption = geometry_result
            except Exception as e:
                geometry_path, geometry_caption = None, None
                print("Erro ao gerar geometria:", e)

        if graph_path:
            resposta = graph_meta.get("message", "Aqui está o gráfico solicitado.")
        elif geometry_path:
            resposta = geometry_caption or "Aqui está a demonstração visual."
        elif clean_text and is_smalltalk(clean_text) and not uploaded_files:
            resposta = greeting_reply()
        else:
            try:
                use_vision_now = should_use_vision(clean_text, image_paths)

                if not clean_text and image_paths:
                    prompt = (
                        "O professor enviou uma imagem. "
                        "Responda de forma breve dizendo que a imagem foi recebida "
                        "e peça o que exatamente ele quer analisar nela."
                    )
                    resposta = ask_vision_ai(prompt, image_paths[0])
                else:
                    prompt = build_prompt(
                        user_input=clean_text or "Analise o material anexado.",
                        mentor=area,
                        profile="Professor",
                        history=st.session_state.chat_history[:-1],
                        context_text=transient_context_text,
                        context_file_name=transient_context_file_name,
                        context_file_type=transient_context_file_type,
                    )

                    if use_vision_now and image_paths:
                        resposta = ask_vision_ai(prompt, image_paths[0])
                    else:
                        resposta = ask_ai(prompt)

                if not resposta:
                    resposta = "Tive um problema ao responder agora. Pode repetir?"

            except Exception as e:
                resposta = f"Erro ao gerar resposta: {e}"

        image_path = graph_path or geometry_path

        assistant_item = {
            "role": "assistant",
            "content": resposta,
            "image_path": image_path,
        }

        st.session_state.chat_history.append(assistant_item)
        save_message(cid, "assistant", resposta, image_path=image_path)

        st.rerun()


# =========================================================
# RENDER
# =========================================================
if not st.session_state.logged:
    render_welcome_screen()
elif st.session_state.page == "masters":
    render_masters_screen()
elif st.session_state.page == "chat":
    render_chat_screen()
else:
    render_welcome_screen()

render_global_footer()
