import base64
import html
import mimetypes
import os
from functools import lru_cache

import streamlit as st
from masters import MASTERS


def render_sidebar_brand():
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Bridge to the Future</div>
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
            <div class="landing-title">Bridge to the Future</div>
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
            <div class="history-title">{html.escape(str(title))}</div>
            <div class="history-meta">{html.escape(str(updated_at)[:16].replace("T", " "))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@lru_cache(maxsize=32)
def _image_to_data_url(path: str) -> str:
    if not path or not os.path.exists(path):
        return ""

    mime, _ = mimetypes.guess_type(path)
    mime = mime or "image/png"

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


def _assistant_avatar_data_url() -> str:
    selected_area = st.session_state.get("selected_area")
    if not selected_area:
        return ""

    data = MASTERS.get(selected_area, {})
    image_path = data.get("image", "")
    return _image_to_data_url(image_path)


def render_message(item: dict):
    role = item.get("role", "assistant")
    content = item.get("content", "") or ""
    image_path = item.get("image_path")
    attachment_labels = item.get("attachment_labels", []) or []

    is_user = role == "user"

    row_class = "msg-row msg-row-user" if is_user else "msg-row msg-row-assistant"
    bubble_class = "msg-bubble msg-bubble-user" if is_user else "msg-bubble msg-bubble-assistant"
    avatar_class = "msg-avatar msg-avatar-user" if is_user else "msg-avatar msg-avatar-assistant"
    meta_label = "Professor" if is_user else "Mestre"

    has_text = bool(content.strip())
    has_image = bool(image_path and os.path.exists(image_path))
    has_attachments = bool(attachment_labels)

    assistant_avatar = _assistant_avatar_data_url()

    st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)

    if not is_user:
        if assistant_avatar:
            st.markdown(
                f'<div class="{avatar_class}" style="background-image: url(\'{assistant_avatar}\');"></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(f'<div class="{avatar_class}">M</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="{bubble_class}">', unsafe_allow_html=True)
    st.markdown(f'<div class="msg-meta">{meta_label}</div>', unsafe_allow_html=True)

    if has_text:
        st.markdown('<div class="msg-markdown">', unsafe_allow_html=True)
        st.markdown(content, unsafe_allow_html=False)
        st.markdown('</div>', unsafe_allow_html=True)

    if has_attachments:
        for label in attachment_labels:
            st.markdown(
                f'<div class="msg-attachment">{html.escape(str(label))}</div>',
                unsafe_allow_html=True,
            )

    if has_image:
        st.image(image_path, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if is_user:
        st.markdown(f'<div class="{avatar_class}">P</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


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
