import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0a0a0a;
        --bg-soft: #0f1115;
        --panel: #111317;
        --panel-2: #171a21;
        --panel-3: #1d2230;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.14);
        --text: #f3f4f6;
        --muted: #a7afbf;
        --accent: #8ab4f8;
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.38);
        --glow: radial-gradient(circle at top left, rgba(66, 133, 244, 0.10), transparent 34%);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .stApp {
        background:
            var(--glow),
            linear-gradient(180deg, #090909 0%, #0b0d12 52%, #090909 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 2rem;
    }

    /* esconde elementos do Streamlit */
    #MainMenu,
    header[data-testid="stHeader"],
    footer,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0 !important;
        position: fixed !important;
    }

    /* sidebar */
    [data-testid="stSidebar"] {
        background:
            radial-gradient(circle at top left, rgba(66, 133, 244, 0.10), transparent 28%),
            linear-gradient(180deg, #0d1016 0%, #0a0c11 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    /* wrappers */
    .chat-main-wrap {
        max-width: 980px;
        margin: 0 auto;
        padding-bottom: 1rem;
    }

    .chat-topbar {
        background:
            linear-gradient(135deg, rgba(25, 30, 42, 0.94), rgba(17, 20, 28, 0.94));
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.35rem 1.4rem;
        margin-bottom: 1.15rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }

    .chat-topbar::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top left, rgba(138, 180, 248, 0.10), transparent 34%);
        pointer-events: none;
    }

    .chat-topbar-title {
        position: relative;
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }

    .chat-topbar-meta {
        position: relative;
        color: #b7c0d1;
        font-size: 1.02rem;
        font-weight: 500;
    }

    .context-chip {
        background: rgba(20, 24, 31, 0.94);
        border: 1px solid var(--border);
        color: var(--text);
        border-radius: 16px;
        padding: 0.86rem 1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.22);
    }

    /* histórico */
    .history-card {
        background: linear-gradient(135deg, rgba(25, 30, 42, 0.94), rgba(18, 22, 31, 0.94));
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1rem;
        margin-bottom: 0.6rem;
        transition: 0.2s ease;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.18);
    }

    .history-card:hover {
        border-color: var(--border-strong);
        transform: translateY(-1px);
    }

    .history-card.active {
        background: linear-gradient(135deg, rgba(31, 38, 53, 0.96), rgba(21, 26, 36, 0.96));
        border-color: rgba(138, 180, 248, 0.32);
        box-shadow: 0 0 0 1px rgba(138, 180, 248, 0.12), 0 14px 30px rgba(0, 0, 0, 0.22);
    }

    .history-title {
        font-weight: 700;
        font-size: 0.99rem;
        color: #f5f7fb;
        letter-spacing: -0.02em;
    }

    .history-meta {
        color: var(--muted);
        font-size: 0.83rem;
        margin-top: 0.22rem;
    }

    /* textos gerais */
    .stMarkdown, .stText, .stCaption, .stAlert,
    label, p, li, span, small, h1, h2, h3, h4, h5, h6 {
        color: var(--text);
    }

    .stCaption {
        color: var(--muted) !important;
    }

    /* inputs */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div,
    [data-baseweb="input"] {
        background: rgba(28, 31, 39, 0.96) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: rgba(138, 180, 248, 0.38) !important;
        box-shadow: 0 0 0 1px rgba(138, 180, 248, 0.18);
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #8f97a8 !important;
    }

    /* botões */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(180deg, #1c212b 0%, #181c24 100%);
        color: #f4f6fb;
        border: 1px solid var(--border);
        border-radius: 16px;
        min-height: 3rem;
        font-weight: 600;
        transition: 0.18s ease;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.18);
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(180deg, #242a36 0%, #1c2230 100%);
        border-color: rgba(138, 180, 248, 0.25);
        color: #ffffff;
        transform: translateY(-1px);
    }

    /* expander / alerts */
    div[data-testid="stExpander"] {
        background: rgba(20, 24, 31, 0.92);
        border: 1px solid var(--border);
        border-radius: 16px;
    }

    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 16px;
        background: rgba(20, 24, 31, 0.94);
        border: 1px solid var(--border);
    }

    /* uploader */
    section[data-testid="stFileUploaderDropzone"] {
        background: rgba(20, 24, 31, 0.92);
        border: 1px dashed rgba(138, 180, 248, 0.22);
        border-radius: 18px;
    }

    /* chat */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    [data-testid="stChatInput"] {
        background: transparent;
    }

    [data-testid="stChatInput"] > div {
        background: linear-gradient(180deg, rgba(19, 22, 29, 0.96), rgba(16, 18, 24, 0.96));
        border: 1px solid var(--border);
        border-radius: 22px;
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

    /* links */
    a {
        color: var(--accent) !important;
    }

    hr {
        border-color: var(--border);
    }

    /* KaTeX / LaTeX */
    .katex, .katex * {
        font-family: KaTeX_Main, Times New Roman, serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
