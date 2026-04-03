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

    profile = st.radio(
        "Perfil",
        ["Aluno", "Professor"],
        horizontal=True,
        key="home_profile",
    )

    cols = st.columns(2)
    for i, area in enumerate(areas):
        data = MENTORS[area]
        with cols[i % 2]:
            st.markdown(
                f"""
                <div style="
                    background: rgba(255,255,255,0.72);
                    border: 1px solid rgba(120,90,60,0.12);
                    border-radius: 18px;
                    padding: 18px;
                    min-height: 170px;
                    margin-bottom: 14px;
                ">
                    <div style="font-size: 1.15rem; font-weight: 800; margin-bottom: 6px;">
                        {data.get("emoji", "")} {data.get("title", area)}
                    </div>
                    <div style="opacity: 0.85; line-height: 1.45;">
                        {data.get("description", "")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(f"Entrar em {area}", key=f"enter_{area}", use_container_width=True):
                open_area(area, profile)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =========================================================
# TELA INICIAL
# =========================================================
if st.session_state.page == "home":
    render_home()

# =========================================================
# CHAT
# =========================================================
area = st.session_state.selected_area
area_info = MENTORS[area]

if st.session_state.current_conversation_id is None:
    cid = get_active_conversation_id(area) or ensure_default_conversation(area)
    st.session_state.current_conversation_id = cid
    st.session_state.chat_history = load_messages_for_conversation(cid)

sidebar, main = st.columns([1.1, 4.2], gap="medium")

# =========================================================
# SIDEBAR
# =========================================================
with sidebar:
    if os.path.exists("logoifce.png"):
        st.image("logoifce.png", width=110)

    st.markdown("### Bridge to the Future")
    st.caption(f"{area_info.get('title', area)}")

    st.radio(
        "Perfil",
        ["Aluno", "Professor"],
        horizontal=True,
        key="profile_sidebar",
    )
    st.session_state.profile = st.session_state.profile_sidebar

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Voltar", use_container_width=True):
            go_home()
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

            st.markdown(
                f"""
                <div style="
                    background: {'rgba(166,124,82,0.18)' if active else 'rgba(255,255,255,0.55)'};
                    border: 1px solid rgba(120,90,60,0.14);
                    border-radius: 14px;
                    padding: 10px 12px;
                    margin-bottom: 8px;
                ">
                    <div style="font-weight: 700; font-size: 0.95rem;">
                        {conv["title"]}
                    </div>
                    <div style="font-size: 0.78rem; opacity: 0.75;">
                        {str(conv["updated_at"])[:16].replace('T', ' ')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Abrir", key=f"open_conv_{conv['id']}", use_container_width=True):
                open_conversation(conv["id"])

    if st.session_state.profile == "Professor":
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
# MAIN
# =========================================================
with main:
    top_left, top_right = st.columns([4.3, 1.3], gap="medium")

    with top_left:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,250,243,0.95) 0%, rgba(243,229,214,0.92) 100%);
                border: 1px solid rgba(120,90,60,0.14);
                border-radius: 22px;
                padding: 22px;
                margin-bottom: 14px;
            ">
                <div style="font-size: 2rem; font-weight: 900; margin-bottom: 6px;">
                    Bridge to the Future
                </div>
                <div style="opacity: 0.82; margin-bottom: 14px;">
                    Projeto educacional para estudantes da rede pública.
                </div>
                <div style="
                    background: rgba(255,255,255,0.72);
                    border: 1px solid rgba(120,90,60,0.12);
                    border-radius: 16px;
                    padding: 14px;
                ">
                    <div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 4px;">
                        {area_info.get("title", area)}
                    </div>
                    <div style="opacity: 0.84;">
                        {area_info.get("description", "")}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_right:
        if os.path.exists("logoprojeto.png"):
            st.image("logoprojeto.png", use_container_width=True)

    if st.session_state.profile == "Professor" and st.session_state.show_materials_panel:
        render_materials_admin(default_subject=area)

    if st.session_state.context_file_name:
        st.markdown(
            f"""
            <div style="
                background: rgba(255,255,255,0.65);
                border: 1px solid rgba(120,90,60,0.14);
                border-radius: 14px;
                padding: 12px 14px;
                margin-bottom: 14px;
            ">
                <b>Contexto ativo:</b> {st.session_state.context_file_name} • {st.session_state.context_file_type}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # mensagens
    for item in st.session_state.chat_history:
        render_message(item)

    # barra de ações
    act1, act2, _ = st.columns([1.1, 1.2, 4.7])
    with act1:
        if st.button("📎 Anexar", use_container_width=True):
            st.session_state.show_attach_panel = not st.session_state.show_attach_panel
            st.rerun()

    with act2:
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
            key=f"uploader_{area}",
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

    user_input = st.chat_input(f"Converse com a área de {area.lower()}...")

    if user_input:
        cid = st.session_state.current_conversation_id

        user_item = {"role": "user", "content": user_input}
        st.session_state.chat_history.append(user_item)
        save_message(cid, "user", user_input)

        # gráfico
        graph_path = None
        graph_meta = {}

        try:
            graph_result = maybe_generate_graph(user_input, area)
            if graph_result is not None and isinstance(graph_result, tuple) and len(graph_result) == 2:
                graph_path, graph_meta = graph_result
        except Exception as e:
            graph_path, graph_meta = None, {}
            print("Erro ao gerar gráfico:", e)

        # geometria
        geometry_path = None
        geometry_caption = None

        try:
            geometry_result = maybe_generate_geometry_visual(user_input, area)
            if geometry_result is not None and isinstance(geometry_result, tuple) and len(geometry_result) == 2:
                geometry_path, geometry_caption = geometry_result
        except Exception as e:
            geometry_path, geometry_caption = None, None
            print("Erro ao gerar visual geométrico:", e)

        # decisão da resposta
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
                    profile=st.session_state.profile,
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
