import html
import os

import streamlit as st
from masters import MASTERS


def render_sidebar_brand():
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Bridge to the Future Project</div>
            <div class="sidebar-sub">Plataforma educacional em evolução.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_landing_screen(masters: dict, on_open):
    st.markdown('<div class="landing-wrap">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="landing-hero">
            <div class="landing-title">Bridge to the Future Project</div>
            <div class="landing-sub">
                Escolha uma área para entrar no seu ambiente de estudo.
                Cada mestre possui contexto, histórico e base de conteúdo próprios.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    master_items = list(masters.items())
    cols = st.columns(2, gap="medium")

    for i, (name, data) in enumerate(master_items):
        with cols[i % 2]:
            st.markdown('<div class="landing-card">', unsafe_allow_html=True)

            image_path = data.get("image", "")
            if image_path and os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                fallback_text = str(data.get("emoji", "DOC"))
                st.markdown(
                    f"""
                    <div class="landing-image-fallback">
                        <div class="landing-fallback-inner">{fallback_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            title = str(data.get("title", name))
            desc = str(data.get("description", ""))

            st.markdown(
                f"""
                <div class="landing-name">{title}</div>
                <div class="landing-desc">{desc}</div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

            if st.button(
                f"Entrar em {name}",
                key=f"open_{name}",
                use_container_width=True,
            ):
                on_open(name)

    st.markdown("</div>", unsafe_allow_html=True)


def _assistant_avatar():
    selected_area = st.session_state.get("selected_area")
    if not selected_area:
        return ":material/school:"

    data = MASTERS.get(selected_area, {})
    image_path = data.get("image", "")
    if image_path and os.path.exists(image_path):
        return image_path

    return ":material/school:"


def render_message(item: dict):
    role = item.get("role", "assistant")
    content = item.get("content", "") or ""
    image_path = item.get("image_path")
    attachment_labels = item.get("attachment_labels", []) or []

    is_user = role == "user"
    message_name = "user" if is_user else "assistant"
    avatar = ":material/person:" if is_user else _assistant_avatar()
    role_label = "Professor" if is_user else "Mestre"

    with st.chat_message(message_name, avatar=avatar):
        st.markdown(
            f'<div class="message-role-pill">{html.escape(role_label)}</div>',
            unsafe_allow_html=True,
        )

        if content.strip():
            st.markdown(content, unsafe_allow_html=False)

        for label in attachment_labels:
            st.markdown(
                f'<div class="message-attachment-pill">{html.escape(str(label))}</div>',
                unsafe_allow_html=True,
            )

        if image_path and os.path.exists(image_path):
            st.image(image_path, use_container_width=True)


def render_context_chip(file_name: str, file_type: str):
    st.markdown(
        f"""
        <div class="context-chip">
            <b>Contexto ativo:</b> {html.escape(str(file_name))} • {html.escape(str(file_type))}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_topbar(master_title: str, professor_name: str):
    st.markdown(
        f"""
        <div class="chat-sticky-top">
            <div class="chat-sticky-master">{html.escape(str(master_title))}</div>
            <div class="chat-sticky-professor">Professor {html.escape(str(professor_name))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
