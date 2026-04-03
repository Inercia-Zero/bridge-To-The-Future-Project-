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
from ui_components import (
    render_landing_screen,
    render_sidebar_brand,
    render_chat_header,
    render_history_item,
    render_message,
    render_context_chip,
)
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

DEFAULTS = {
    "screen": "landing",
    "selected_mentor": None,
    "profile": "Aluno",
    "current_conversation_id": None,
    "chat_history": [],
    "show_materials_panel": False,
    "show_attach_panel": False,
    "context_file_path": None,
    "context_file_name": None,
    "context_file_type": None,
    "context_text": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def open_mentor(mentor: str):
    st.session_state.selected_mentor = mentor
    st.session_state.screen = "chat"
    cid = ensure_default_conversation(mentor)
    st.session_state.current_conversation_id = cid
    st.session_state.chat_history = load_messages_for_conversation(cid)
    st.session_state.show_attach_panel = False
    st.session_state.show_materials_panel = False
    st.session_state.context_file_path = None
    st.session_state.context_file_name = None
    st.session_state.context_file_type = None
    st.session_state.context_text = None
    st.rerun()


def go_home():
    st.session_state.screen = "landing"
    st.session_state.selected_mentor = None
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


if st.session_state.screen == "landing":
    render_landing_screen(MENTORS, open_mentor)
    st.stop()

mentor = st.session_state.selected_mentor
mentor_info = MENTORS[mentor]

if st.session_state.current_conversation_id is None:
    cid = get_active_conversation_id(mentor) or ensure_default_conversation(mentor)
    st.session_state.current_conversation_id = cid
    st.session_state.chat_history = load_messages_for_conversation(cid)

sidebar, main = st.columns([1.05, 4.2], gap="medium")

with sidebar:
    render_sidebar_brand()

    st.session_state.profile = st.radio(
        "Perfil",
        ["Aluno", "Professor"],
        horizontal=True,
        key="profile_radio_visual",
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Voltar", use_container_width=True):
            go_home()
    with c2:
        if st.button("Nova", use_container_width=True):
            new_id = create_new_conversation(mentor)
            st.session_state.current_conversation_id = new_id
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("### Histórico")
    conversations = list_conversations_by_mentor(mentor)
    if not conversations:
        st.caption("Nenhuma conversa ainda.")
    else:
        for item in conversations:
            render_history_item(
                title=item["title"],
                updated_at=item["updated_at"],
                active=item["id"] == st.session_state.current_conversation_id,
            )
            if st.button("Abrir", key=f"abrir_{item['id']}", use_container_width=True):
                open_conversation(item["id"])

    if st.session_state.profile == "Professor":
        st.markdown("---")
        if st.button("Base docente", use_container_width=True):
            st.session_state.show_materials_panel = not st.session_state.show_materials_panel
            st.rerun()

        with st.expander("Materiais recentes", expanded=False):
            rows = list_materials(limit=8, subject=mentor)
            if rows:
                for row in rows:
                    st.markdown(f"**{row['title']}**")
                    st.caption(f"{row['subject']} • {row['teacher_name'] or 'Professor não informado'}")
            else:
                st.caption("Nenhum material cadastrado.")

with main:
    render_chat_header(
        project_title="Bridge to the Future",
        subtitle="Projeto educacional para estudantes da rede pública.",
        mentor_title=mentor_info["title"],
        mentor_description=mentor_info["description"],
        mentor_key=mentor,
    )

    if st.session_state.profile == "Professor" and st.session_state.show_materials_panel:
        render_materials_admin(default_subject=mentor)

    if st.session_state.context_file_name:
        render_context_chip(
            st.session_state.context_file_name,
            st.session_state.context_file_type,
        )

    for item in st.session_state.chat_history:
        render_message(item)

    with st.container():
        t1, t2, _ = st.columns([1.1, 1.2, 4.7])

        with t1:
            if st.button("📎 Anexar", use_container_width=True):
                st.session_state.show_attach_panel = not st.session_state.show_attach_panel
                st.rerun()

        with t2:
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
                key=f"uploader_{mentor}",
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

    user_input = st.chat_input(f"Converse com o mentor de {mentor.lower()}...")

    if user_input:
        cid = st.session_state.current_conversation_id

        user_item = {"role": "user", "content": user_input}
        st.session_state.chat_history.append(user_item)
        save_message(cid, "user", user_input)

        graph_path = None
        graph_meta = {}

        try:
            graph_result = maybe_generate_graph(user_input, mentor)

            if graph_result is not None and isinstance(graph_result, tuple) and len(graph_result) == 2:
                graph_path, graph_meta = graph_result
            else:
                graph_path, graph_meta = None, {}

        except Exception as e:
            graph_path, graph_meta = None, {}
            print("Erro ao gerar gráfico:", e)

        geometry_path = None
        geometry_caption = None

        try:
            geometry_result = maybe_generate_geometry_visual(user_input, mentor)

            if geometry_result is not None and isinstance(geometry_result, tuple) and len(geometry_result) == 2:
                geometry_path, geometry_caption = geometry_result
            else:
                geometry_path, geometry_caption = None, None

        except Exception as e:
            geometry_path, geometry_caption = None, None
            print("Erro ao gerar visual geométrico:", e)

        if graph_path:
            resposta = graph_meta.get("message", "Aqui está o gráfico solicitado.")

        elif geometry_path:
            resposta = geometry_caption or "Aqui está a demonstração visual."

        elif is_smalltalk(user_input):
            respostas = [
                "E aí! Bora estudar o quê?",
                "Fala! O que você quer aprender hoje?",
                "Manda a dúvida 😄",
                "Bora! Qual é o desafio?",
                "Pode perguntar sem medo 👊",
                "Aqui não tem erro... só cálculo 😂"
            ]
            resposta = random.choice(respostas)
            
        else:
            try:
                prompt = build_prompt(
                    user_input=user_input,
                    mentor=mentor,
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
                    resposta = "Tive um problema ao responder, mas ainda estou aqui. Pode repetir?"

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
