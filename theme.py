import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    :root {
        --bg: #212121;
        --panel: #171717;
        --panel-2: #2a2a2a;
        --panel-3: #303030;
        --border: #3a3a3a;
        --text: #ececec;
        --muted: #b4b4b4;
        --accent: #10a37f;
        --accent-hover: #0d8f6f;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    html, body, [class*="css"] {
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: var(--panel);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    .chat-main-wrap {
        max-width: 980px;
        margin: 0 auto;
        padding-bottom: 1rem;
    }

    .chat-topbar {
        background: rgba(42, 42, 42, 0.92);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1.15rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
    }

    .chat-topbar-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--text);
    }

    .chat-topbar-meta {
        margin-top: 0.2rem;
        color: var(--muted);
        font-size: 0.92rem;
    }

    .context-chip {
        background: rgba(42, 42, 42, 0.95);
        border: 1px solid var(--border);
        color: var(--text);
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
    }

    .history-card {
        background: var(--panel-2);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.85rem 0.95rem;
        margin-bottom: 0.55rem;
    }

    .history-card.active {
        border-color: #5a5a5a;
        background: var(--panel-3);
    }

    .history-title {
        font-weight: 700;
        color: var(--text);
    }

    .history-meta {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: 0.18rem;
    }

    [data-testid="stChatMessage"] {
        background: var(--panel-2);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.75rem;
    }

    [data-testid="stChatMessage"] * {
        color: var(--text);
    }

    .stButton > button {
        background: var(--panel-2);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 12px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: var(--panel-3);
        border-color: #555555;
        color: #ffffff;
    }

    .stDownloadButton > button {
        background: var(--panel-2);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {
        background: #2f2f2f !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #9a9a9a !important;
    }

    [data-baseweb="input"] {
        background: #2f2f2f !important;
    }

    .stMarkdown,
    .stCaption,
    .stAlert,
    .stExpander,
    label,
    p,
    li,
    span,
    small {
        color: var(--text);
    }

    .stCaption {
        color: var(--muted) !important;
    }

    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 14px;
    }

    div[data-testid="stExpander"] {
        background: var(--panel-2);
        border: 1px solid var(--border);
        border-radius: 14px;
    }

    .stFileUploader {
        background: transparent;
    }

    section[data-testid="stFileUploaderDropzone"] {
        background: var(--panel-2);
        border: 1px dashed #5b5b5b;
        border-radius: 16px;
    }

    [data-testid="stChatInput"] {
        background: transparent;
    }

    [data-testid="stChatInput"] textarea {
        background: #2f2f2f !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
    }

    [data-testid="stToolbar"] {
        right: 1rem;
    }

    a {
        color: #8ab4f8 !important;
    }

    hr {
        border-color: var(--border);
    }
    </style>
    """, unsafe_allow_html=True)
