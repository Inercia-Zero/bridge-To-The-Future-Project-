import os
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
    render_sidebar_brand,
    render_landing_screen,
    render_hero,
    render_mentor_cards,
    render_chat_bubble,
    render_context_box,
    render_conversation_list,
)
from materials import render_materials_admin
from attachments import validate_upload, save_upload, extract_pdf_text
from graph_tools import maybe_generate_graph

st.set_page_config(
    page_title="Bridge to the Future",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_db()
init_materials_table()

defaults = {
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
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def open_mentor(mentor: str):
    st.session_state.selected_mentor = mentor
    st.session_state.screen = "chat"
    cid = ensure_default_conversation(mentor)
    st.session_state.current_conversation_id = cid
    st.session_state.chat_history = load_messages_for_conversation(cid)
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

with st.sidebar:
    render_sidebar_brand()
    st.session_state.profile = st.radio("Perfil", ["Aluno", "Professor"], horizontal=True)

    top1, top2 = st.columns(2)
    with top1:
        if st.button("Voltar", use_container_width=True):
            go_home()
    with top2:
        if st.button("Nova conversa", use_container_width=True):
            new_id = create_new_conversation(mentor)
            st.session_state.current_conversation_id = new_id
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("### Histórico do mentor")
    conversations = list_conversations_by_mentor(mentor)
    render_conversation_list(
        conversations=conversations,
        current_conversation_id=st.session_state.current_conversation_id,
        on_open=open_conversation,
    )

    if st.session_state.profile == "Professor":
        st.markdown("---")
        if st.button("Base docente", use_container_width=True):
            st.session_state.show_materials_panel = not st.session_state.show_materials_panel
            st.rerun()

        with st.expander("Materiais mais recentes", expanded=False):
            rows = list_materials(limit=8, subject=mentor)
            if rows:
                for row in rows:
                    st.markdown(
                        f"**{row['title']}**  \n"
                        f"<span class='small-muted'>{row['subject']} • {row['teacher_name'] or 'Professor não informado'}</span>",
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("Nenhum material cadastrado ainda.")

render_hero(
    project_title="Bridge to the Future",
    subtitle="Projeto educacional para estudantes da rede pública.",
    mentor_title=mentor_info["title"],
    mentor_description=mentor_info["description"],
    mentor_key=mentor,
)

render_mentor_cards(MENTORS, active_mentor=mentor)

if st.session_state.profile == "Professor" and st.session_state.show_materials_panel:
    render_materials_admin(default_subject=mentor)

if st.session_state.context_file_name:
    render_context_box(st.session_state.context_file_name, st.session_state.context_file_type)

for item in st.session_state.chat_history:
    with st.chat_message(item["role"]):
        render_chat_bubble(item["content"], role=item["role"])
        if item.get("image_path") and os.path.exists(item["image_path"]):
            st.image(item["image_path"], use_container_width=True)

attach_col1, attach_col2, attach_col3 = st.columns([1.2, 4, 1.4])
with attach_col1:
    if st.button("📎 Anexar", use_container_width=True):
        st.session_state.show_attach_panel = not st.session_state.show_attach_panel
        st.rerun()
with attach_col3:
    if st.session_state.context_file_name and st.button("Remover anexo", use_container_width=True):
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
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    save_message(cid, "user", user_input)

    with st.chat_message("user"):
        render_chat_bubble(user_input, role="user")

    generated_graph = maybe_generate_graph(user_input, mentor)

    with st.chat_message("assistant"):
        if is_smalltalk(user_input):
            resposta = mentor_info["smalltalk"]
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
            except Exception as e:
                resposta = f"Erro ao gerar resposta: {e}"

        render_chat_bubble(resposta, role="assistant")

        if generated_graph and os.path.exists(generated_graph):
            st.image(generated_graph, caption="Gráfico gerado", use_container_width=True)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": resposta,
                "image_path": generated_graph,
            }
        )
        save_message(cid, "assistant", resposta, image_path=generated_graph)
