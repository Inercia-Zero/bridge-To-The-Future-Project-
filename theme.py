import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    :root {
        --bg: #141414;
        --bg-2: #171717;
        --bg-3: #1b1b1b;
        --sidebar: #161616;
        --panel: #1f1f1f;
        --panel-2: #232323;
        --panel-3: #2a2a2a;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.14);
        --text: #ececec;
        --muted: #a8a8a8;
        --muted-2: #8c8c8c;
        --shadow: 0 12px 32px rgba(0, 0, 0, 0.22);
        --radius-lg: 22px;
        --radius-md: 16px;
        --radius-sm: 12px;
    }

    html, body {
        background: var(--bg) !important;
        color: var(--text);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", Arial, sans-serif;
    }

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
        padding-top: 1rem;
        padding-bottom: 1rem;
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

    .sidebar-brand-title {
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #f4f4f4;
    }

    .sidebar-brand-sub {
        margin-top: 0.28rem;
        color: #d7d7d7;
        font-weight: 600;
        font-size: 0.98rem;
    }

    .sidebar-brand-user {
        margin-top: 0.5rem;
        color: var(--muted);
        font-size: 0.92rem;
    }

    .welcome-brand {
        text-align: center;
        margin-top: 24px;
        margin-bottom: 10px;
    }

    .welcome-brand-title {
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: #f4f4f4;
    }

    .welcome-brand-subtitle {
        opacity: 0.82;
        margin-top: 6px;
        color: var(--muted);
    }

    .stMarkdown, .stText, .stCaption, .stAlert,
    label, p, li, span, small, h1, h2, h3, h4, h5, h6 {
        color: var(--text) !important;
    }

    .stCaption {
        color: var(--muted) !important;
    }

    a {
        color: #dddddd !important;
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
        top: 0.6rem;
        z-index: 25;
        background: rgba(27, 27, 27, 0.92) !important;
        backdrop-filter: blur(10px);
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg);
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }

    .chat-topbar-title {
        font-size: 1.86rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #f4f4f4 !important;
        line-height: 1.08;
    }

    .chat-topbar-meta {
        margin-top: 0.36rem;
        color: #c5c5c5 !important;
        font-size: 1.02rem;
        font-weight: 600;
    }

    .context-chip {
        background: linear-gradient(180deg, #1e1e1e 0%, #191919 100%) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: var(--radius-md);
        padding: 0.82rem 1rem;
        margin-bottom: 0.85rem;
    }

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

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-bottom: 0.1rem;
    }

    .msg-row {
        display: flex;
        align-items: flex-end;
        gap: 0.8rem;
        width: 100%;
        margin: 0.35rem 0 1rem 0;
    }

    .msg-row-user {
        justify-content: flex-end;
    }

    .msg-row-assistant {
        justify-content: flex-start;
    }

    .msg-avatar {
        flex: 0 0 42px;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: #2a2a2a;
        color: #f4f4f4;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        border: 1px solid var(--border);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        box-shadow: 0 6px 16px rgba(0,0,0,0.16);
    }

    .msg-avatar-user {
        background: linear-gradient(180deg, #2b2b2b 0%, #222222 100%);
    }

    .msg-avatar-assistant {
        background-color: #1f1f1f;
    }

    .msg-bubble {
        max-width: min(78%, 760px);
        padding: 0.95rem 1rem;
        border-radius: 22px;
        border: 1px solid var(--border);
        box-shadow: 0 10px 24px rgba(0,0,0,0.12);
    }

    .msg-bubble-user {
        background: linear-gradient(180deg, #262626 0%, #202020 100%) !important;
        border-bottom-right-radius: 10px;
    }

    .msg-bubble-assistant {
        background: linear-gradient(180deg, #1d1d1d 0%, #181818 100%) !important;
        border-bottom-left-radius: 10px;
    }

    .msg-meta {
        font-size: 0.78rem;
        font-weight: 800;
        color: #bcbcbc !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.55rem;
    }

    .msg-markdown {
        color: var(--text) !important;
        line-height: 1.64 !important;
        font-size: 1rem !important;
    }

    .msg-markdown p:last-child {
        margin-bottom: 0 !important;
    }

    .msg-markdown ul,
    .msg-markdown ol {
        margin-bottom: 0.6rem !important;
    }

    .msg-attachment {
        margin-top: 0.7rem;
        padding: 0.65rem 0.8rem;
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: 12px;
        color: var(--muted) !important;
        font-size: 0.92rem;
    }

    .stChatFloatingInputContainer,
    [data-testid="stBottom"],
    div[data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottomBlockContainer"] > div,
    [data-testid="stChatInputContainer"],
    [data-testid="ScrollToBottomContainer"] {
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
    .msg-markdown pre {
        background: #1b1b1b !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }

    .stMarkdown code,
    .msg-markdown code {
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
    </style>
    """, unsafe_allow_html=True)
