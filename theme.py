import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    :root {
        --bg: #141414;
        --bg-2: #171717;
        --sidebar: #161616;
        --panel: #1f1f1f;
        --panel-2: #232323;
        --panel-3: #2a2a2a;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.14);
        --text: #ececec;
        --muted: #a8a8a8;
        --muted-2: #8c8c8c;
        --shadow: 0 10px 28px rgba(0, 0, 0, 0.22);
        --radius-lg: 22px;
        --radius-md: 16px;
    }

    html, body {
        background: var(--bg) !important;
        color: var(--text);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", Arial, sans-serif;
    }

    /* FUNDO GLOBAL SEM AZUL */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main,
    section.main,
    .block-container {
        background: var(--bg) !important;
        color: var(--text) !important;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 1.1rem;
        padding-bottom: 1rem;
    }

    /* ESCONDE O QUE NÃO PRESTA, MAS NÃO O HEADER */
    #MainMenu,
    footer,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        height: 0 !important;
        position: fixed !important;
    }

    /* HEADER MANTIDO PARA A SETA DA SIDEBAR */
    header[data-testid="stHeader"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: 3rem !important;
    }

    header[data-testid="stHeader"] * {
        color: var(--text) !important;
    }

    /* BOTÕES DO HEADER / SIDEBAR */
    header[data-testid="stHeader"] button,
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] button,
    button[aria-label*="sidebar"],
    button[title*="sidebar"] {
        background: #242424 !important;
        color: #f2f2f2 !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16) !important;
    }

    header[data-testid="stHeader"] button:hover,
    [data-testid="collapsedControl"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover,
    button[aria-label*="sidebar"]:hover,
    button[title*="sidebar"]:hover {
        background: #2d2d2d !important;
        border-color: var(--border-strong) !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171717 0%, #141414 100%) !important;
        border-right: 1px solid var(--border) !important;
    }

    [data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    /* TEXTO GERAL */
    .stMarkdown, .stText, .stCaption, .stAlert,
    label, p, li, span, small, h1, h2, h3, h4, h5, h6 {
        color: var(--text) !important;
    }

    .stCaption {
        color: var(--muted) !important;
    }

    a {
        color: #d8d8d8 !important;
        text-decoration: none;
    }

    hr {
        border-color: var(--border) !important;
    }

    /* WRAPPERS */
    .chat-main-wrap {
        max-width: 980px;
        margin: 0 auto;
        padding-bottom: 1rem;
        background: transparent !important;
    }

    .chat-topbar {
        background: linear-gradient(180deg, #202020 0%, #1b1b1b 100%) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg);
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.15rem;
        box-shadow: var(--shadow);
    }

    .chat-topbar-title {
        font-size: 1.72rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #f4f4f4 !important;
        line-height: 1.08;
    }

    .chat-topbar-meta {
        margin-top: 0.42rem;
        color: #b7b7b7 !important;
        font-size: 1rem;
        font-weight: 500;
    }

    .context-chip {
        background: linear-gradient(180deg, #1e1e1e 0%, #191919 100%) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: var(--radius-md);
        padding: 0.82rem 1rem;
        margin-bottom: 0.85rem;
    }

    /* HISTÓRICO */
    .history-card {
        background: linear-gradient(180deg, #252525 0%, #202020 100%) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.55rem;
        transition: 0.18s ease;
        box-shadow: 0 6px 16px rgba(0,0,0,0.14);
    }

    .history-card:hover {
        background: linear-gradient(180deg, #2b2b2b 0%, #232323 100%) !important;
        border-color: var(--border-strong) !important;
        transform: translateY(-1px);
    }

    .history-card.active {
        background: linear-gradient(180deg, #2d2d2d 0%, #252525 100%) !important;
        border-color: rgba(255,255,255,0.16) !important;
    }

    .history-title {
        font-weight: 700;
        font-size: 1rem;
        color: #f1f1f1 !important;
        letter-spacing: -0.02em;
    }

    .history-meta {
        color: var(--muted) !important;
        font-size: 0.82rem;
        margin-top: 0.24rem;
    }

    /* INPUTS */
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

    /* BOTÕES */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(180deg, #2a2a2a 0%, #242424 100%) !important;
        color: #f2f2f2 !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        min-height: 3rem;
        font-weight: 600;
        transition: 0.18s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(180deg, #313131 0%, #2a2a2a 100%) !important;
        border-color: var(--border-strong) !important;
        color: #ffffff !important;
    }

    /* ALERTAS / EXPANDER */
    div[data-testid="stExpander"] {
        background: #1d1d1d !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
    }

    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 16px !important;
        background: #1d1d1d !important;
        border: 1px solid var(--border) !important;
    }

    section[data-testid="stFileUploaderDropzone"] {
        background: #1c1c1c !important;
        border: 1px dashed rgba(255,255,255,0.12) !important;
        border-radius: 18px !important;
    }

    /* MENSAGENS DO CHAT */
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
        background: transparent !important;
    }

    /* TIRA A BARRA/FUNDO AZUL DO BLOCO INFERIOR */
    .stChatFloatingInputContainer,
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottomBlockContainer"] > div,
    [data-testid="stChatInputContainer"],
    [data-testid="ScrollToBottomContainer"],
    [data-testid="stChatInput"] + div {
        background: transparent !important;
        background-color: transparent !important;
        border-top: none !important;
        box-shadow: none !important;
    }

    /* INPUT DO CHAT */
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

    /* CÓDIGO */
    .stMarkdown pre {
        background: #1b1b1b !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }

    .stMarkdown code {
        color: #efefef !important;
    }

    /* LATEX */
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
        letter-spacing: normal !important;
        word-spacing: normal !important;
        text-transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
