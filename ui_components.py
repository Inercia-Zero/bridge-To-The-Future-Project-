
import os
import streamlit as st

def render_sidebar_brand():
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    if os.path.exists("logoifce.png"):
        st.image("logoifce.png", width=110)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=110)
    st.markdown('<div class="sidebar-title">Bridge to the Future</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Plataforma educacional em evolução.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_landing_screen(mentors: dict, on_open):
    st.markdown('<div class="landing-wrap">', unsafe_allow_html=True)
    if os.path.exists("logoifce.png"):
        c1, c2, c3 = st.columns([1.4, 1.2, 1.4])
        with c2:
            st.image("logoifce.png", width=160)

    st.markdown(
        """
        <div class="landing-hero">
            <div class="landing-title">Bridge to the Future</div>
            <div class="landing-sub">
                Escolha uma área para entrar no seu ambiente de estudo.
                Cada mentor possui contexto, histórico e base de conteúdo próprios.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    mentor_items = list(mentors.items())
    for i, (name, data) in enumerate(mentor_items):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="landing-card">
                    <div class="landing-emoji">{data.get('emoji', '')}</div>
                    <div class="landing-name">{name}</div>
                    <div class="landing-desc">{data.get('description', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.button(f"Entrar em {name}", key=f"open_{name}", use_container_width=True, on_click=on_open, args=(name,))
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat_header(project_title: str, subtitle: str, mentor_title: str, mentor_description: str, mentor_key: str):
    left, right = st.columns([4.3, 1.2])
    with left:
        st.markdown(
            f"""
            <div class="chat-header-card">
                <div class="chat-title">{project_title}</div>
                <div class="chat-sub">{subtitle}</div>
                <div class="chat-mentor-box">
                    <div class="chat-mentor-title">{mentor_title}</div>
                    <div class="small-muted">{mentor_description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        if os.path.exists("logoprojeto.png"):
            st.image("logoprojeto.png", use_container_width=True)

def render_history_item(title: str, updated_at: str, active: bool):
    css = "history-card active" if active else "history-card"
    st.markdown(
        f"""
        <div class="{css}">
            <div class="history-title">{title}</div>
            <div class="history-meta">{updated_at[:16].replace('T', ' ')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_message(item: dict):
    role = item.get("role", "assistant")
    css = "message-card message-user" if role == "user" else "message-card message-assistant"
    st.markdown(f'<div class="{css}">{item.get("content","")}</div>', unsafe_allow_html=True)
    if item.get("image_path") and os.path.exists(item["image_path"]):
        st.image(item["image_path"], use_container_width=True)

def render_context_chip(file_name: str, file_type: str):
    st.markdown(
        f"""
        <div class="context-chip">
            <b>Contexto ativo:</b> {file_name} • {file_type}
        </div>
        """,
        unsafe_allow_html=True,
    )
