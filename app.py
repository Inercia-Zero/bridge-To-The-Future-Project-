import os
import streamlit as st

from theme import apply_theme
from mentors import MENTORS
from database import init_db, init_materials_table, list_materials
from prompts import build_prompt
from groq_client import ask_ai, ask_vision_ai
from ui_components import (
    render_sidebar_brand,
    render_hero,
    render_mentor_cards,
    render_chat_bubble,
    render_context_box,
)
from materials import render_materials_admin
from attachments import (
    validate_upload,
    save_upload,
    extract_pdf_text,
)
from graph_tools import maybe_generate_graph

st.set_page_config(
    page_title="Bridge to the Future",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_db()
init_materials_table()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mentor" not in st.session_state:
    st.session_state.mentor = "Matemática"
if "profile" not in st.session_state:
    st.session_state.profile = "Aluno"
if "show_materials_panel" not in st.session_state:
    st.session_state.show_materials_panel = False
if "context_file_path" not in st.session_state:
    st.session_state.context_file_path = None
if "context_file_name" not in st.session_state:
    st.session_state.context_file_name = None
if "context_file_type" not in st.session_state:
    st.session_state.context_file_type = None
if "context_text" not in st.session_state:
    st.session_state.context_text = None

with st.sidebar:
    render_sidebar_brand()
    st.session_state.profile = st.radio("Perfil", ["Aluno", "Professor"], horizontal=True)
    st.session_state.mentor = st.selectbox(
        "Escolha o mentor",
        list(MENTORS.keys()),
        index=list(MENTORS.keys()).index(st.session_state.mentor),
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Nova conversa", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with c2:
        if st.button("Base docente", use_container_width=True):
            st.session_state.show_materials_panel = not st.session_state.show_materials_panel
            st.rerun()

    st.markdown("### Contexto da conversa")
    uploaded = st.file_uploader(
        "Anexe PDF, imagem ou TXT",
        type=["pdf", "png", "jpg", "jpeg", "webp", "txt"],
        key="main_context_uploader",
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

    if st.session_state.context_file_name:
        render_context_box(
            st.session_state.context_file_name,
            st.session_state.context_file_type,
        )
        if st.button("Remover contexto", use_container_width=True):
            st.session_state.context_file_path = None
            st.session_state.context_file_name = None
            st.session_state.context_file_type = None
            st.session_state.context_text = None
            st.rerun()

    with st.expander("Materiais cadastrados", expanded=False):
        rows = list_materials(limit=8)
        if rows:
            for row in rows:
                st.markdown(
                    f"**{row['title']}**  \n"
                    f"<span class='small-muted'>{row['subject']} • {row['teacher_name'] or 'Professor não informado'}</span>",
                    unsafe_allow_html=True,
                )
        else:
            st.caption("Nenhum material cadastrado ainda.")

mentor_info = MENTORS[st.session_state.mentor]

render_hero(
    project_title="Bridge to the Future",
    subtitle="Projeto educacional para estudantes da rede pública.",
    mentor_title=mentor_info["title"],
    mentor_description=mentor_info["description"],
)

render_mentor_cards(MENTORS, active_mentor=st.session_state.mentor)

if st.session_state.show_materials_panel:
    render_materials_admin()

for item in st.session_state.chat_history:
    with st.chat_message(item["role"]):
        render_chat_bubble(item["content"], role=item["role"])
        if item.get("image_path") and os.path.exists(item["image_path"]):
            st.image(item["image_path"], use_container_width=True)

user_input = st.chat_input("Digite sua dúvida, peça uma explicação, envie contexto ou solicite um gráfico...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        render_chat_bubble(user_input, role="user")

    generated_graph = maybe_generate_graph(user_input, st.session_state.mentor)

    with st.chat_message("assistant"):
        try:
            prompt = build_prompt(
                user_input=user_input,
                mentor=st.session_state.mentor,
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
        except Exception as e:
            resposta = f"Erro ao gerar resposta: {e}"

        render_chat_bubble(resposta, role="assistant")
        graph_path = generated_graph
        if graph_path and os.path.exists(graph_path):
            st.image(graph_path, caption="Gráfico gerado", use_container_width=True)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": resposta,
                "image_path": graph_path,
            }
        )
