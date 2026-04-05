import random
from pathlib import Path

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
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================
def get_owner() -> str:
    return (st.session_state.get("display_name") or "").strip().lower()


def format_person_name(name: str) -> str:
    name = (name or "").strip()
    if not name:
        return ""
    return " ".join(part[:1].upper() + part[1:].lower() for part in name.split())


def get_professor_label() -> str:
    owner = get_owner()
    formatted = format_person_name(owner)
    return f"Professor {formatted}" if formatted else "Professor"


def get_master_label(area: str) -> str:
    return f"Mestre de {area}" if area else "Mestre"


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
    st.rerun()


def open_conversation(conversation_id: int):
    st.session_state.current_conversation_id = conversation_id
    st.session_state.chat_history = load_messages_for_conversation(conversation_id)
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
        <div class="welcome-brand-wrap">
            <div class="welcome-brand-title">Bridge to the Future</div>
            <div class="welcome-brand-sub">
                Projeto educacional para docentes da rede pública
            </div>
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


def normalize_chat_submission(submission):
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


def process_uploaded_files(uploaded_files):
    attached_labels = []
    image_paths = []
    saved_items = []

    if not uploaded_files:
        return {
            "attached_labels": attached_labels,
            "image_paths": image_paths,
            "saved_items": saved_items,
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

    # Apenas PDF/TXT ativam contexto persistente
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
        "saved_items": saved_items,
    }


def render_chat_bubble(item: dict):
    role = item.get("role", "assistant")
    content = (item.get("content") or "").strip()
    image_path = item.get("image_path")
    attachment_labels = item.get("attachment_labels", [])

    wrapper_class = "chat-row user-row" if role == "user" else "chat-row assistant-row"
    bubble_class = "chat-bubble user-bubble" if role == "user" else "chat-bubble assistant-bubble"

    html_parts = [f'<div class="{wrapper_class}"><div class="{bubble_class}">']

    if content:
        safe_content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_content = safe_content.replace("\n", "<br>")
        html_parts.append(f'<div class="bubble-text">{safe_content}</div>')

    if attachment_labels:
        html_parts.append('<div class="bubble-attachments">')
        for label in attachment_labels:
            safe_label = label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_parts.append(f'<div class="attachment-line">{safe_label}</div>')
        html_parts.append("</div>")

    html_parts.append("</div></div>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)

    if image_path and Path(image_path).exists():
        image_col_left, image_col_mid, image_col_right = st.columns([1, 6, 1])
        target_col = image_col_right if role == "assistant" else image_col_left
        with target_col:
            st.image(image_path, use_container_width=True)


# =========================================================
# TELA 1 - ACESSO
# =========================================================
def render_welcome_screen():
    st.markdown("<div style='max-width: 980px; margin: 0 auto;'>", unsafe_allow_html=True)

    render_top_brand()

    st.markdown("### Acesso")

    username = st.text_input(
        "Usuário",
        value=st.session_state.display_name,
        key="welcome_username",
        placeholder="Ex: seu usuário",
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
        placeholder="Ex: planejar aula, gerar questões, analisar PDF, explicar conteúdo...",
    )

    suggested = suggest_area_from_text(search_text)
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
        f"### Bem-vindo, **{format_person_name(st.session_state.display_name)}**. Escolha seu mestre."
    )

    if st.session_state.selected_area:
        st.info(f"Sugestão com base no que você escreveu: {st.session_state.selected_area}")

    render_landing_screen(MASTERS, open_area)

    c1, _ = st.columns(2)

    with c1:
        if st.button("Sair", use_container_width=True):
            st.session_state.logged = False
            st.session_state.display_name = ""
            st.session_state.selected_area = None
            st.session_state.current_conversation_id = None
            st.session_state.chat_history = []
            st.session_state.show_materials_panel = False
            clear_active_context()
            go_to_welcome()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TELA 3 - CHAT
# =========================================================
def render_chat_screen():
    area = st.session_state.selected_area
    owner = get_owner()

    if not area:
        go_to_masters()
        return

    if st.session_state.current_conversation_id is None:
        cid = get_active_conversation_id(area, owner) or ensure_default_conversation(area, owner)
        st.session_state.current_conversation_id = cid
        st.session_state.chat_history = load_messages_for_conversation(cid)

    # =========================================================
    # SIDEBAR NATIVA
    # =========================================================
    with st.sidebar:
        st.markdown("## Bridge to the Future")
        st.caption(get_master_label(area))
        st.caption(get_professor_label())

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Mestres", use_container_width=True):
                go_to_masters()

        with c2:
            if st.button("Nova", use_container_width=True):
                new_id = create_new_conversation(area, owner)
                st.session_state.current_conversation_id = new_id
                st.session_state.chat_history = []
                st.session_state.show_materials_panel = False
                clear_active_context()
                st.rerun()

        st.markdown("### Histórico")

        conversations = list_conversations_by_mentor(area, owner)
        if not conversations:
            st.caption("Nenhuma conversa ainda.")
        else:
            for conv in conversations:
                active = conv["id"] == st.session_state.current_conversation_id
                css = "history-card active" if active else "history-card"

                st.markdown(
                    f"""
                    <div class="{css}">
                        <div class="history-title">{conv["title"]}</div>
                        <div class="history-meta">{str(conv["updated_at"])[:16].replace('T', ' ')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button("Abrir", key=f"open_conv_{conv['id']}", use_container_width=True):
                    open_conversation(conv["id"])

        st.markdown("---")

        if st.button("Base docente", use_container_width=True):
            st.session_state.show_materials_panel = not st.session_state.show_materials_panel
            st.rerun()

        with st.expander("Materiais recentes", expanded=False):
            rows = list_materials(limit=8, subject=area)
            if rows:
                for row in rows:
                    st.markdown(f"**{row['title']}**")
                    st.caption(f"{row['subject']} • {row['teacher_name'] or 'Professor não informado'}")
            else:
                st.caption("Nenhum material cadastrado.")

    # =========================================================
    # CABEÇALHO FIXO VISUAL DO CHAT
    # =========================================================
    st.markdown(
        f"""
        <div class="sticky-chat-header">
            <div class="sticky-master-title">{get_master_label(area)}</div>
            <div class="sticky-professor-sub">{get_professor_label()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="chat-main-wrap">', unsafe_allow_html=True)

    if st.session_state.show_materials_panel:
        render_materials_admin(default_subject=area)

    if st.session_state.context_file_name:
        st.markdown(
            f"""
            <div class="context-chip">
                <b>Contexto ativo:</b> {st.session_state.context_file_name} • {st.session_state.context_file_type}
            </div>
            """,
            unsafe_allow_html=True,
        )

        cctx1, cctx2 = st.columns([0.24, 0.76])
        with cctx1:
            if st.button("Remover contexto", use_container_width=True):
                clear_active_context()
                st.rerun()
        with cctx2:
            st.markdown("")

    if not st.session_state.chat_history:
        st.markdown(
            """
            <div class="empty-chat-state">
                Comece a conversa com seu mestre. Você também pode anexar PDF, texto ou imagem no campo de mensagem.
            </div>
            """,
            unsafe_allow_html=True,
        )

    for item in st.session_state.chat_history:
        render_chat_bubble(item)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================
    # CHAT INPUT NATIVO
    # =========================================================
    submission = st.chat_input(
        f"Converse com o mestre de {area.lower()}...",
        key="main_chat_input",
        accept_file="multiple",
        file_type=["pdf", "png", "jpg", "jpeg", "webp", "txt"],
    )

    user_input, uploaded_files = normalize_chat_submission(submission)

    if submission is not None:
        cid = st.session_state.current_conversation_id

        attached_labels = []
        image_paths = []

        if uploaded_files:
            try:
                processed = process_uploaded_files(uploaded_files)
                attached_labels = processed["attached_labels"]
                image_paths = processed["image_paths"]
            except Exception as e:
                st.error(f"Erro ao processar arquivo: {e}")
                st.stop()

        clean_text = (user_input or "").strip()
        display_text = clean_text

        non_image_labels = attached_labels[:]
        if image_paths:
            non_image_labels = [
                label for label in attached_labels
                if "IMAGE:" not in label.upper() and "IMAGEM:" not in label.upper()
            ]

        if not display_text and non_image_labels:
            display_text = "\n".join(non_image_labels)
        elif display_text and non_image_labels:
            display_text = f"{display_text}\n\n" + "\n".join(non_image_labels)

        user_item = {
            "role": "user",
            "content": display_text,
            "image_path": image_paths[0] if image_paths else None,
            "attachment_labels": non_image_labels,
        }

        st.session_state.chat_history.append(user_item)
        save_message(
            cid,
            "user",
            display_text,
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
        elif clean_text and is_smalltalk(clean_text):
            resposta = greeting_reply()
        else:
            try:
                use_vision_now = should_use_vision(clean_text, image_paths)

                if not clean_text and image_paths:
                    prompt = (
                        "O professor enviou uma imagem. "
                        "Responda de forma breve confirmando o recebimento e "
                        "peça o que exatamente ele deseja analisar nela."
                    )
                    resposta = ask_vision_ai(prompt, image_paths[0])
                else:
                    prompt = build_prompt(
                        user_input=clean_text or "Analise o material anexado.",
                        mentor=area,
                        profile="Professor",
                        history=st.session_state.chat_history[:-1],
                        context_text=st.session_state.context_text,
                        context_file_name=st.session_state.context_file_name,
                        context_file_type=st.session_state.context_file_type,
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
            "attachment_labels": [],
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
