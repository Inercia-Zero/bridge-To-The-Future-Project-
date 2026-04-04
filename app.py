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


# =========================================================
# ACESSOS
# =========================================================
USERS = {
    "adenilson": "1234",
    "orlando": "1234",
    "francisco": "1234",
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
        "E aí! Bora planejar algo bom?",
        "Fala! O que você quer montar hoje?",
        "Manda a ideia 😄",
        "Bora! Qual conteúdo?",
        "Pode mandar 👊",
    ]
    return random.choice(respostas)


def login_ok(username: str, password: str) -> bool:
    return USERS.get((username or "").strip().lower()) == password


def get_user_subject_key(area: str) -> str:
    user = (st.session_state.display_name or "").strip().lower()
    return f"{area}__{user}"


def go_to_welcome():
    st.session_state.page = "welcome"
    st.rerun()


def go_to_masters():
    st.session_state.page = "masters"
    st.rerun()


def open_area(area: str):
    subject_key = area

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


# =========================================================
# UI AUXILIAR
# =========================================================
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
        placeholder="Ex: adenilson, orlando, francisco...",
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
        f"### Bem-vindo, **{st.session_state.display_name}**. Escolha seu mestre."
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
            go_to_welcome()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TELA 3 - CHAT
# =========================================================
def render_chat_screen():
    area = st.session_state.selected_area

    if not area:
        go_to_masters()
        return

    area_info = MASTERS[area]
    subject_key = get_user_subject_key(area)

    if st.session_state.current_conversation_id is None:
        cid = get_active_conversation_id(area) or ensure_default_conversation(area)
        st.session_state.current_conversation_id = cid
        st.session_state.chat_history = load_messages_for_conversation(cid)

    sidebar, main = st.columns([1.15, 4.2], gap="medium")

    with sidebar:
        st.markdown("### Bridge to the Future")
        st.caption(area_info.get("title", area))
        st.caption(f"Usuário: {st.session_state.display_name}")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Mestres", use_container_width=True):
                go_to_masters()

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

    with main:
        st.markdown(
            f"""
            <div class="chat-header-card">
                <div class="chat-title">Bridge to the Future</div>
                <div class="chat-sub">Projeto educacional para auxílio a docentes da rede pública.</div>
                <div class="chat-mentor-box">
                    <div class="chat-mentor-title">{area_info.get("title", area)}</div>
                    <div class="small-muted">{area_info.get("description", "")}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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

        for item in st.session_state.chat_history:
            render_message(item)

        a1, a2, _ = st.columns([1.1, 1.2, 4.7])

        with a1:
            if st.button("📎 Anexar", use_container_width=True):
                st.session_state.show_attach_panel = not st.session_state.show_attach_panel
                st.rerun()

        with a2:
            if st.session_state.context_file_name and st.button("Remover", use_container_width=True):
                st.session_state.context_file_path = None
                st.session_state.context_file_name = None
                st.session_state.context_file_type = None
                st.session_state.context_text = None
                st.rerun()

        if st.session_state.show_attach_panel:
            uploaded = st.file_uploader(
                "Escolha PDF, imagem ou TXT",
                type=["pdf", "png", "jpg", "jpeg", "webp", "txt"],
                key=f"uploader_{subject_key}",
                label_visibility="collapsed",
            )

            if uploaded is not None:
                error = validate_upload(uploaded)
                if error:
                    st.error(error)
                else:
                    file_path, file_name, file_type = save_upload(uploaded)
                    st.session_state.context_file_path = file_path
                    st.session_state.context_file_name = file_name
                    st.session_state.context_file_type = file_type

                    if file_type == "pdf":
                        st.session_state.context_text = extract_pdf_text(file_path)
                    elif file_type == "text":
                        with open(file_path, "r", encoding="utf-8") as f:
                            st.session_state.context_text = f.read()
                    else:
                        st.session_state.context_text = None

                    st.success(f"Arquivo ativo: {file_name}")

        user_input = st.chat_input(f"Converse com o mestre de {area.lower()}...")

        if user_input:
            cid = st.session_state.current_conversation_id

            user_item = {"role": "user", "content": user_input}
            st.session_state.chat_history.append(user_item)
            save_message(cid, "user", user_input)

            graph_path = None
            graph_meta = {}

            try:
                graph_result = maybe_generate_graph(user_input, area)
                if graph_result is not None and isinstance(graph_result, tuple) and len(graph_result) == 2:
                    graph_path, graph_meta = graph_result
            except Exception as e:
                graph_path, graph_meta = None, {}
                print("Erro ao gerar gráfico:", e)

            geometry_path = None
            geometry_caption = None

            try:
                geometry_result = maybe_generate_geometry_visual(user_input, area)
                if geometry_result is not None and isinstance(geometry_result, tuple) and len(geometry_result) == 2:
                    geometry_path, geometry_caption = geometry_result
            except Exception as e:
                geometry_path, geometry_caption = None, None
                print("Erro ao gerar geometria:", e)

            if graph_path:
                resposta = graph_meta.get("message", "Aqui está o gráfico solicitado.")
            elif geometry_path:
                resposta = geometry_caption or "Aqui está a demonstração visual."
            elif is_smalltalk(user_input):
                resposta = greeting_reply()
            else:
                try:
                    prompt = build_prompt(
                        user_input=user_input,
                        mentor=area,
                        profile="Professor",
                        history=st.session_state.chat_history[:-1],
                        context_text=st.session_state.context_text,
                        context_file_name=st.session_state.context_file_name,
                        context_file_type=st.session_state.context_file_type,
                    )

                    if st.session_state.context_file_type == "image" and st.session_state.context_file_path:
                        resposta = ask_vision_ai(prompt, st.session_state.context_file_path)
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
