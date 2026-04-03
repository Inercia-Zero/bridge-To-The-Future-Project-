import os
import streamlit as st

def render_sidebar_brand():
    st.markdown('<div class="brand-box">', unsafe_allow_html=True)

    if os.path.exists("logoifce.png"):
        st.image("logoifce.png", width=92)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=92)

    st.markdown('<div class="brand-title">Bridge to the Future</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Plataforma educacional em evolução.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_hero(project_title: str, subtitle: str, mentor_title: str, mentor_description: str):
    col1, col2 = st.columns([4, 1.4])
    with col1:
        st.markdown(
            f"""
            <div class="hero-wrap">
                <div class="hero-title">{project_title} 🚀</div>
                <div class="hero-sub">{subtitle}</div>
                <div class="mentor-highlight">
                    <div class="mentor-highlight-title">{mentor_title}</div>
                    <div class="small-muted">{mentor_description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if os.path.exists("logoprojeto.png"):
            st.image("logoprojeto.png", use_container_width=True)

def render_mentor_cards(mentors: dict, active_mentor: str):
    cards = []
    for name, data in mentors.items():
        active_class = "mentor-card active" if name == active_mentor else "mentor-card"
        cards.append(
            f"""
            <div class="{active_class}">
                <div class="mentor-name">{data.get('emoji', '')} {name}</div>
                <div class="mentor-desc">{data.get('description', '')}</div>
            </div>
            """
        )

    st.markdown(f'<div class="mentor-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

def render_chat_bubble(content: str, role: str = "assistant"):
    css_class = "chat-user" if role == "user" else "chat-assistant"
    st.markdown(f'<div class="{css_class}">{content}</div>', unsafe_allow_html=True)

def render_context_box(file_name: str, file_type: str):
    st.markdown(
        f"""
        <div class="context-box">
            <div class="materials-title">Contexto ativo</div>
            <div class="materials-sub"><b>Arquivo:</b> {file_name}<br><b>Tipo:</b> {file_type}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
