import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #141414;
        --bg-2: #1a1a1a;
        --sidebar: #171717;
        --panel: #212121;
        --panel-hover: #2a2a2a;
        --panel-soft: #1e1e1e;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.14);
        --text: #ececec;
        --muted: #a6a6a6;
        --muted-2: #8f8f8f;
        --shadow: 0 10px 28px rgba(0, 0, 0, 0.26);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top center, rgba(255, 255, 255, 0.03), transparent 26%),
            linear-gradient(180deg, var(--bg) 0%, #121212 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 1.6rem;
        max-width: 1280px;
    }

    /* Streamlit chrome */
    #MainMenu,
    header[data-testid="stHeader"],
    footer,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        height: 0 !important;
        position: fixed !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171717 0%, #141414 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        letter-spacing: -0.03em;
    }

    /* General text */
    .stMarkdown, .stText, .stCaption, .stAlert,
    label, p, li, span, small, h1, h2, h3, h4, h5, h6 {
        color: var(--text);
    }

    .stCaption {
        color: var(--muted) !important;
    }

    a {
        color: #c9d7ff !important;
        text-decoration: none;
    }

    /* Main wrappers */
    .chat-main-wrap {
        max-width: 980px;
        margin: 0 auto;
        padding-bottom: 1rem;
    }

    .chat-topbar {
        background: linear-gradient(180deg, #202020 0%, #1c1c1c 100%);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 1.2rem 1.35rem;
        margin-bottom: 1.05rem;
        box-shadow: var(--shadow);
    }

    .chat-topbar-title {
        font-size: 1.72rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #f3f3f3;
        line-height: 1.1;
    }

    .chat-topbar-meta {
        margin-top: 0.42rem;
        color: #b8b8b8;
        font-size: 1rem;
        font-weight: 500;
    }

    .context-chip {
        background: #1d1d1d;
        border: 1px solid var(--border);
        color: var(--text);
        border-radius: 16px;
        padding: 0.82rem 1rem;
        margin-bottom: 0.85rem;
    }

    /* History */
    .history-card {
        background: linear-gradient(180deg, #232323 0%, #1f1f1f 100%);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.55rem;
        transition: 0.18s ease;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.14);
    }

    .history-card:hover {
        background: linear-gradient(180deg, #292929 0%, #232323 100%);
        border-color: var(--border-strong);
        transform: translateY(-1px);
    }

    .history-card.active {
        background: linear-gradient(180deg, #2a2a2a 0%, #242424 100%);
        border-color: rgba(255, 255, 255, 0.16);
    }

    .history-title {
        font-weight: 700;
        font-size: 1rem;
        color: #f0f0f0;
        letter-spacing: -0.02em;
    }

    .history-meta {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: 0.24rem;
    }

    /* Inputs */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div,
    [data-baseweb="input"] {
        background: #1f1f1f !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--muted-2) !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: rgba(255, 255, 255, 0.16) !important;
        box-shadow: none !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(180deg, #2a2a2a 0%, #242424 100%);
        color: #f2f2f2;
        border: 1px solid var(--border);
        border-radius: 16px;
        min-height: 3rem;
        font-weight: 600;
        transition: 0.18s ease;
        box-shadow: none;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(180deg, #313131 0%, #2b2b2b 100%);
        border-color: var(--border-strong);
        color: #ffffff;
    }

    /* Expanders / alerts */
    div[data-testid="stExpander"] {
        background: #1d1d1d;
        border: 1px solid var(--border);
        border-radius: 16px;
    }

    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 16px;
        background: #1e1e1e;
        border: 1px solid var(--border);
    }

    section[data-testid="stFileUploaderDropzone"] {
        background: #1d1d1d;
        border: 1px dashed rgba(255, 255, 255, 0.14);
        border-radius: 18px;
    }

    /* Chat area */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-bottom: 0.25rem;
    }

    [data-testid="stChatInput"] {
        background: transparent;
    }

    [data-testid="stChatInput"] > div {
        background: linear-gradient(180deg, #232323 0%, #1f1f1f 100%);
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: var(--shadow);
    }

    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: var(--text) !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 18px !important;
        font-size: 1rem !important;
    }

    [data-testid="stChatInput"] button {
        border-radius: 16px !important;
    }

    /* Divider */
    hr {
        border-color: var(--border);
    }

    /* Keep LaTeX safe */
    .katex, .katex * {
        font-family: KaTeX_Main, Times New Roman, serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
