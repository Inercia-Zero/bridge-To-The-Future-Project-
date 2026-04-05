import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    :root {
        --bg: #141414;
        --bg-2: #171717;
        --bg-3: #1c1c1c;
        --panel: #1f1f1f;
        --panel-2: #232323;
        --panel-3: #2b2b2b;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.14);
        --text: #ececec;
        --muted: #a8a8a8;
        --muted-2: #8c8c8c;
        --shadow: 0 12px 28px rgba(0, 0, 0, 0.20);
        --radius-lg: 22px;
        --radius-md: 16px;
        --radius-sm: 12px;
    }

    html, body {
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", Arial, sans-serif;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main,
    section.main,
    .block-container,
    [data-testid="stVerticalBlock"],
    [data-testid="stApp"] {
        background: var(--bg) !important;
        color: var(--text) !important;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 0.9rem;
        padding-bottom: 3.6rem;
    }

    #MainMenu,
    footer,
    div[data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        height: 0 !important;
        position: fixed !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    div[data-testid="stToolbar"] {
        background: transparent !important;
        border: none !important;
    }

    div[data-testid="stToolbar"] button,
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

    div[data-testid="stToolbar"] button:hover,
    header[data-testid="stHeader"] button:hover,
    [data-testid="collapsedControl"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover,
    button[aria-label*="sidebar"]:hover,
    button[title*="sidebar"]:hover {
        background: #2d2d2d !important;
        border-color: var(--border-strong) !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171717 0%, #141414 100%) !important;
        border-right: 1px solid var(--border) !important;
    }

    [data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    .sidebar-brand {
        background: linear-gradient(180deg, #202020 0%, #1a1a1a 100%);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }

    .sidebar-brand-kicker {
        color: #d0d0d0;
        font-size: 0.76rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        margin-bottom: 0.35rem;
    }

    .sidebar-brand-title {
        font-size: 1.28rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        color: #f4f4f4;
        line-height: 1.08;
    }

    .sidebar-brand-user {
        margin-top: 0.55rem;
        color: var(--muted);
        font-size: 0.96rem;
        font-weight: 600;
    }

    .welcome-brand {
        text-align: center;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .welcome-brand-title {
        font-size: 2.55rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: #f4f4f4;
    }

    .welcome-brand-subtitle {
        opacity: 0.86;
        margin-top: 7px;
        color: var(--muted);
        font-size: 1rem;
    }

    .stMarkdown, .stText, .stCaption, .stAlert,
    label, p, li, span, small, h1, h2, h3, h4, h5, h6 {
        color: var(--text) !important;
    }

    .stCaption {
        color: var(--muted) !important;
    }

    a {
        color: #e0e0e0 !important;
        text-decoration: none;
    }

    hr {
        border-color: var(--border) !important;
    }

    .chat-main-wrap {
        max-width: 980px;
        margin: 0 auto;
        padding-bottom: 1rem;
        background: transparent !important;
    }

    .chat-topbar {
        position: sticky;
        top: 0.55rem;
        z-index: 20;
        text-align: center;
        background: rgba(28, 28, 28, 0.96) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg);
        padding: 1rem 1.25rem 1.05rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        backdrop-filter: blur(8px);
    }

    .chat-topbar-kicker {
        color: #d0d0d0 !important;
        font-size: 0.76rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        margin-bottom: 0.32rem;
    }

    .chat-topbar-title {
        font-size: 1.9rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: #f4f4f4 !important;
        line-height: 1.06;
    }

    .chat-topbar-meta {
        margin-top: 0.38rem;
        color: #c4c4c4 !important;
        font-size: 1rem;
        font-weight: 700;
    }

    .context-chip {
        background: linear-gradient(180deg, #1e1e1e 0%, #191919 100%) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: var(--radius-md);
        padding: 0.82rem 1rem;
        margin-bottom: 0.85rem;
    }

    .history-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.05);
        margin: 0.2rem 0 0.65rem 0;
    }

    .landing-wrap {
        padding-bottom: 1rem;
    }

    .landing-hero {
        background: linear-gradient(180deg, #202020 0%, #1a1a1a 100%);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.2rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }

    .landing-title {
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: #f4f4f4;
    }

    .landing-sub {
        margin-top: 0.4rem;
        color: var(--muted);
        line-height: 1.55;
    }

    .landing-card {
        background: linear-gradient(180deg, #202020 0%, #1a1a1a 100%);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 1rem;
        margin-bottom: 0.7rem;
        box-shadow: var(--shadow);
    }

    .landing-image-fallback {
        background: linear-gradient(180deg, #2a2a2a 0%, #232323 100%);
        border: 1px solid var(--border);
        border-radius: 18px;
        min-height: 190px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.85rem;
    }

    .landing-fallback-inner {
        font-size: 2rem;
        font-weight: 900;
        color: #efefef;
    }

    .landing-name {
        font-size: 1.14rem;
        font-weight: 800;
        color: #f2f2f2;
        margin-top: 0.2rem;
    }

    .landing-desc {
        margin-top: 0.35rem;
        color: var(--muted);
        line-height: 1.55;
    }

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

    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(180deg, #2a2a2a 0%, #242424 100%) !important;
        color: #f2f2f2 !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        min-height: 2.9rem;
        font-weight: 600;
        transition: 0.18s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(180deg, #313131 0%, #2a2a2a 100%) !important;
        border-color: var(--border-strong) !important;
        color: #ffffff !important;
    }

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

    /* Histórico da sidebar mais limpo */
    [data-testid="stSidebar"] .stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
        min-height: 2.65rem;
    }

    /* Popover do menu */
    [data-testid="stPopover"] button {
        min-height: 2.4rem !important;
    }

    /* Chat */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-bottom: 0.3rem;
    }

    [data-testid="stChatMessageContent"] {
        background: linear-gradient(180deg, #202020 0%, #1a1a1a 100%) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 0.85rem 1rem !important;
        box-shadow: 0 10px 22px rgba(0,0,0,0.12);
    }

    .message-role-pill {
        display: inline-block;
        margin-bottom: 0.65rem;
        padding: 0.28rem 0.58rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #d6d6d6 !important;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.07);
    }

    .message-attachment-pill {
        margin-top: 0.75rem;
        padding: 0.68rem 0.84rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border);
        color: var(--muted) !important;
        font-size: 0.92rem;
    }

    /* Mata a mancha/faixa azul do bloco inferior */
    .stChatFloatingInputContainer,
    [data-testid="stBottom"],
    div[data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottomBlockContainer"] > div,
    [data-testid="stChatInputContainer"],
    [data-testid="ScrollToBottomContainer"],
    [data-testid="stBottomBlockContainer"] section,
    [data-testid="stBottomBlockContainer"] section > div {
        background: var(--bg) !important;
        background-color: var(--bg) !important;
        border-top: none !important;
        box-shadow: none !important;
    }

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

    .stMarkdown pre,
    [data-testid="stChatMessageContent"] pre {
        background: #1b1b1b !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }

    .stMarkdown code,
    [data-testid="stChatMessageContent"] code {
        color: #efefef !important;
    }

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

    .app-footer-fixed {
        position: fixed;
        right: 1rem;
        bottom: 0.7rem;
        z-index: 30;
        display: flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.5rem 0.72rem;
        border-radius: 999px;
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid rgba(255,255,255,0.07);
        color: #cfcfcf;
        font-size: 0.82rem;
        font-weight: 600;
        backdrop-filter: blur(8px);
        box-shadow: 0 10px 24px rgba(0,0,0,0.14);
        pointer-events: none;
    }

    .app-footer-sep {
        color: #8f8f8f;
    }

    @media (max-width: 768px) {
        .chat-topbar-title {
            font-size: 1.55rem;
        }

        .welcome-brand-title,
        .landing-title {
            font-size: 2rem;
        }

        .app-footer-fixed {
            right: 0.6rem;
            left: 0.6rem;
            justify-content: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)
