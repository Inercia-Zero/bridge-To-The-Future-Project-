import os
import streamlit as st


def render_sidebar_brand():
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Bridge to the Future</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Plataforma educacional em evolução.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_landing_screen(masters: dict, on_open):
    st.markdown('<div class="landing-wrap">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="landing-hero">
            <div class="landing-title">Bridge to the Future</div>
            <div class="landing-sub">
                Escolha uma área para entrar no seu ambiente de estudo.
                Cada mestre possui contexto, histórico e base de conteúdo próprios.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    master_items = list(masters.items())

    for i, (name, data) in enumerate(master_items):
        with cols[i % 2]:
            st.markdown('<div class="landing-card">', unsafe_allow_html=True)

            image_path = data.get("image", "")
            if image_path and os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                st.markdown(
                    f"""
                    <div class="landing-image-fallback">
                        {data.get('emoji', '📘')}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <div class="landing-name">{data.get('title', name)}</div>
                <div class="landing-desc">{data.get('description', '')}</div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown('</div>', unsafe_allow_html=True)

            if st.button(
                f"Entrar em {name}",
                key=f"open_{name}",
                use_container_width=True,
            ):
                on_open(name)

    st.markdown('</div>', unsafe_allow_html=True)


def render_chat_header(project_title: str, subtitle: str, master_title: str, master_description: str, master_key: str):
    st.markdown(
        f"""
        <div class="chat-header-card">
            <div class="chat-title">{project_title}</div>
            <div class="chat-sub">{subtitle}</div>
            <div class="chat-mentor-box">
                <div class="chat-mentor-title">{master_title}</div>
                <div class="small-muted">{master_description}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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

    st.markdown(
        f'<div class="{css}">{item.get("content", "")}</div>',
        unsafe_allow_html=True,
    )

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
