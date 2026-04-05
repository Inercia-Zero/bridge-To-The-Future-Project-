import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    :root {
        --bg: #141414;
        --bg-soft: #181818;
        --sidebar: #171717;
        --panel: #1f1f1f;
        --panel-2: #232323;
        --panel-3: #2a2a2a;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.14);
        --text: #ececec;
        --muted: #a8a8a8;
        --muted-2: #8b8b8b;
        --shadow: 0 10px 28px rgba(0, 0, 0, 0.26);
        --radius-lg: 22px;
        --radius-md: 16px;
        --radius-sm: 12px;
    }

    html, body {
        background: var(--bg);
        color: var(--text);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
            Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", Arial, sans-serif;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top center, rgba(255,255,255,0.025), transparent 22%),
            linear-gradient(180deg, #141414 0%, #121212 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 1280px;
        padding-top: 1.4rem;
        padding-bottom: 1rem;
    }

    /* Esconde elementos chatos do Streamlit, mas mantém o controle da sidebar */
    #MainMenu,
    footer,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        height: 0 !important;
        position: fixed !important;
    }

    /* Header transparente para não sumir a seta da sidebar */
    header[data-testid="stHeader"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    header[data-testid="stHeader"] button[kind="header"] {
        background: rgba(35, 35, 35, 0.92) !important;
        color: #f0f0f0 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.18) !important;
    }

    header[data-testid="stHeader"] button[kind="header"]:hover {
        background: rgba(46, 46, 46, 0.96) !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
    }

    /* sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171717 0%, #141414 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    /* texto geral */
    .stMarkdown, .stText, .stCaption, .stAlert,
    label, p, li, span, small, h1, h2, h3, h4, h5, h6 {
        color: var(--text);
    }

    .stCaption {
        color: var(--muted) !important;
    }

    a {
        color: #d7d7d7 !important;
        text-decoration: none;
    }

    hr {
        border-color: var(--border);
    }

    /* wrappers principais */
    .chat-main-wrap {
        max-width: 980px;
        margin: 0 auto;
        padding-bottom: 1rem;
    }

    .chat-topbar {
        background: linear-gradient(180deg, #202020 0%, #1b1b1b 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.15rem;
        box-shadow: var(--shadow);
    }

    .chat-topbar-title {
        font-size: 1.72rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #f4f4f4;
        line-height: 1.08;
    }

    .chat-topbar-meta {
        margin-top: 0.42rem;
        color: #b7b7b7;
        font-size: 1rem;
        font-weight: 500;
    }

    .context-chip {
        background: linear-gradient(180deg, #1e1e1e 0%, #191919 100%);
        border: 1px solid var(--border);
        color: var(--text);
        border-radius: var(--radius-md);
        padding: 0.82rem 1rem;
        margin-bottom: 0.85rem;
    }

    /* histórico */
    .history-card {
        background: linear-gradient(180deg, #252525 0%, #202020 100%);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.55rem;
        transition: 0.18s ease;
        box-shadow: 0 6px 16px rgba(0,0,0,0.14);
    }

    .history-card:hover {
        background: linear-gradient(180deg, #2b2b2b 0%, #232323 100%);
        border-color: var(--border-strong);
        transform: translateY(-1px);
    }

    .history-card.active {
        background: linear-gradient(180deg, #2d2d2d 0%, #252525 100%);
        border-color: rgba(255,255,255,0.16);
    }

    .history-title {
        font-weight: 700;
        font-size: 1rem;
        color: #f1f1f1;
        letter-spacing: -0.02em;
    }

    .history-meta {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: 0.24rem;
    }

    /* inputs */
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
        border-color: rgba(255,255,255,0.16) !important;
        box-shadow: none !important;
    }

    /* botões */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(180deg, #2a2a2a 0%, #242424 100%);
        color: #f2f2f2;
        border: 1px solid var(--border);
        border-radius: 16px;
        min-height: 3rem;
        font-weight: 600;
        transition: 0.18s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(180deg, #313131 0%, #2a2a2a 100%);
        border-color: var(--border-strong);
        color: #ffffff;
    }

    /* expander / alerts */
    div[data-testid="stExpander"] {
        background: #1d1d1d;
        border: 1px solid var(--border);
        border-radius: 16px;
    }

    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 16px;
        background: #1d1d1d;
        border: 1px solid var(--border);
    }

    section[data-testid="stFileUploaderDropzone"] {
        background: #1c1c1c;
        border: 1px dashed rgba(255,255,255,0.12);
        border-radius: 18px;
    }

    /* chat geral */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-bottom: 0.55rem;
    }

    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        line-height: 1.6;
        font-size: 1rem;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        color: #ececec !important;
    }

    /* remove a faixa azul/escura atrás do chat input */
    .stChatFloatingInputContainer,
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottomBlockContainer"] > div,
    [data-testid="stChatInputContainer"] {
        background: transparent !important;
        border-top: none !important;
        box-shadow: none !important;
    }

    /* input do chat */
    [data-testid="stChatInput"] {
        background: transparent !important;
        margin-top: 0.8rem;
    }

    [data-testid="stChatInput"] > div {
        background: linear-gradient(180deg, #232323 0%, #1f1f1f 100%) !important;
        border: 1px solid var(--border) !important;
        border-radius: 24px !important;
        box-shadow: var(--shadow) !important;
    }

    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: var(--text) !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 18px !important;
        font-size: 1rem !important;
        line-height: 1.45 !important;
    }

    [data-testid="stChatInput"] button {
        border-radius: 16px !important;
        background: #2e2e2e !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    [data-testid="stChatInput"] button:hover {
        background: #383838 !important;
    }

    /* blocos markdown comuns */
    .stMarkdown pre {
        background: #1b1b1b !important;
        border: 1px solid var(--border);
        border-radius: 14px;
    }

    .stMarkdown code {
        color: #efefef;
    }

    /* LaTeX preservado */
    .katex-display {
        overflow-x: auto;
        overflow-y: hidden;
        padding: 0.35rem 0;
    }

    .katex, .katex * {
        font-family: KaTeX_Main, "Times New Roman", serif !important;
        letter-spacing: normal !important;
        word-spacing: normal !important;
        text-transform: none !important;
    }

    mjx-container, mjx-container * {
        font-family: inherit !important;
        letter-spacing: normal !important;
        word-spacing: normal !important;
        text-transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
