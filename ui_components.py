import os
import streamlit as st

def render_sidebar_brand():
    st.markdown('<div class="brand-box">', unsafe_allow_html=True)
    if os.path.exists("logoifce.png"):
        st.image("logoifce.png", width=110)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=110)
    st.markdown('<div class="brand-title">Bridge to the Future</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Plataforma educacional em evolução.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_landing_screen(mentors: dict, on_open):
    st.markdown('<div class="landing-wrap">', unsafe_allow_html=True)
    if os.path.exists("logoifce.png"):
        c1, c2, c3 = st.columns([1.5, 1.2, 1.5])
        with c2:
            st.image("logoifce.png", width=150)

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
            if st.button(f"Entrar em {name}", key=f"open_{name}", use_container_width=True):
                on_open(name)
    st.markdown('</div>', unsafe_allow_html=True)

def render_hero(project_title: str, subtitle: str, mentor_title: str, mentor_description: str, mentor_key: str):
    col1, col2 = st.columns([4.2, 1.3])
    with col1:
        st.markdown(
            f"""
            <div class="hero-wrap">
                <div class="hero-title">{project_title}</div>
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

def render_conversation_list(conversations, current_conversation_id, on_open):
    if not conversations:
        st.caption("Nenhuma conversa ainda.")
        return

    for item in conversations:
        active_class = "history-card active" if item["id"] == current_conversation_id else "history-card"
        st.markdown(
            f"""
            <div class="{active_class}">
                <div class="history-title">{item['title']}</div>
                <div class="history-meta">{item['updated_at'][:16].replace('T', ' ')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Abrir", key=f"open_conv_{item['id']}", use_container_width=True):
            on_open(item["id"])
