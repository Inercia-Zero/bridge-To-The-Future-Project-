import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #0f1115;
            --bg-elev: #171a21;
            --panel: #1b1f27;
            --panel-2: #232936;
            --panel-3: #2b3240;
            --border: #313846;
            --border-strong: #414a5d;
            --text: #eef2f7;
            --muted: #a9b3c4;
            --soft: #8b96aa;
            --accent: #7aa2ff;
            --accent-2: #5f8dff;
            --success: #1f9d72;
            --danger: #d25b6a;
            --shadow: 0 10px 28px rgba(0, 0, 0, 0.28);
            --radius: 18px;
            --radius-sm: 12px;
            --ui-font: Inter, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }

        /* ===== Hide Streamlit chrome ===== */
        #MainMenu,
        header,
        footer,
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        .stDeployButton {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }

        /* ===== Base ===== */
        html, body, .stApp {
            background: radial-gradient(circle at top, #181c24 0%, var(--bg) 38%, #0c0e13 100%);
            color: var(--text);
        }

        body,
        .stApp,
        .stMarkdown,
        .stTextInput,
        .stTextArea,
        .stSelectbox,
        .stMultiSelect,
        .stButton,
        .stCaption,
        .stAlert,
        .stChatInput,
        [data-baseweb="input"],
        [data-baseweb="select"],
        label,
        input,
        textarea,
        button,
        p,
        li,
        span,
        small,
        div {
            font-family: var(--ui-font);
        }

        /* Preserve math/code rendering */
        .katex, .katex *, mjx-container, mjx-container *, code, pre, pre *, code * {
            font-family: inherit;
        }

        ::selection {
            background: rgba(122, 162, 255, 0.22);
            color: #ffffff;
        }

        /* ===== Layout ===== */
        .block-container {
            max-width: 1180px;
            padding-top: 1.2rem;
            padding-bottom: 1.25rem;
        }

        .chat-main-wrap {
            max-width: 960px;
            margin: 0 auto;
            padding-bottom: 1rem;
        }

        /* ===== Sidebar ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #131721 0%, #11141c 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }

        [data-testid="stSidebar"] * {
            color: var(--text) !important;
        }

        /* ===== Titles ===== */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text) !important;
            letter-spacing: -0.02em;
            line-height: 1.08;
        }

        h1 { font-weight: 800; }
        h2, h3 { font-weight: 750; }

        p, li {
            line-height: 1.62;
        }

        .stCaption,
        .history-meta,
        .chat-topbar-meta {
            color: var(--muted) !important;
        }

        /* ===== Top brand / custom cards ===== */
        .chat-topbar {
            background: linear-gradient(180deg, rgba(31, 36, 46, 0.98) 0%, rgba(24, 28, 36, 0.98) 100%);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 22px;
            padding: 1.15rem 1.2rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow);
        }

        .chat-topbar-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text);
        }

        .chat-topbar-meta {
            margin-top: 0.24rem;
            font-size: 0.93rem;
        }

        .context-chip {
            background: rgba(28, 33, 43, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.07);
            color: var(--text);
            border-radius: 16px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.9rem;
        }

        .history-card {
            background: linear-gradient(180deg, rgba(35, 41, 54, 0.92) 0%, rgba(28, 33, 43, 0.92) 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 15px;
            padding: 0.9rem 0.95rem;
            margin-bottom: 0.6rem;
        }

        .history-card.active {
            border-color: rgba(122, 162, 255, 0.34);
            box-shadow: 0 0 0 1px rgba(122, 162, 255, 0.10) inset;
        }

        .history-title {
            font-weight: 700;
            color: var(--text);
        }

        /* ===== Generic containers ===== */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlockBorderWrapper"]:has(.stAlert),
        div[data-testid="stExpander"],
        section[data-testid="stFileUploaderDropzone"] {
            border-radius: 16px;
        }

        div[data-testid="stExpander"] {
            background: rgba(28, 33, 43, 0.82);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        /* ===== Inputs ===== */
        .stTextInput input,
        .stTextArea textarea,
        [data-baseweb="input"] input,
        [data-baseweb="base-input"] input,
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {
            background: rgba(36, 42, 53, 0.96) !important;
            color: var(--text) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            min-height: 48px;
            box-shadow: none !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        [data-baseweb="input"] input:focus,
        .stSelectbox div[data-baseweb="select"] > div:focus-within,
        .stMultiSelect div[data-baseweb="select"] > div:focus-within {
            border-color: rgba(122, 162, 255, 0.5) !important;
            box-shadow: 0 0 0 1px rgba(122, 162, 255, 0.18) inset !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: var(--soft) !important;
        }

        /* ===== Buttons ===== */
        .stButton > button,
        .stDownloadButton > button {
            background: linear-gradient(180deg, rgba(43, 50, 64, 0.98) 0%, rgba(34, 40, 52, 0.98) 100%);
            color: var(--text);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            min-height: 44px;
            font-weight: 650;
            transition: 0.18s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: rgba(122, 162, 255, 0.28);
            background: linear-gradient(180deg, rgba(49, 57, 73, 1) 0%, rgba(39, 46, 60, 1) 100%);
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* ===== Alerts ===== */
        .stInfo, .stSuccess, .stWarning, .stError {
            border-radius: 16px;
            border-width: 1px;
        }

        /* ===== Chat input ===== */
        [data-testid="stChatInput"] {
            background: transparent !important;
        }

        [data-testid="stChatInput"] > div {
            background: linear-gradient(180deg, rgba(28, 33, 43, 0.98) 0%, rgba(23, 27, 35, 0.98) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.07) !important;
            border-radius: 20px !important;
            box-shadow: var(--shadow);
        }

        [data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: var(--text) !important;
            border: 0 !important;
            border-radius: 18px !important;
            min-height: 56px !important;
            font-size: 1rem !important;
        }

        [data-testid="stChatInput"] button {
            border-radius: 14px !important;
        }

        /* ===== Native st.chat_message, if used ===== */
        [data-testid="stChatMessage"] {
            background: linear-gradient(180deg, rgba(29, 34, 44, 0.96) 0%, rgba(24, 29, 37, 0.96) 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 18px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16);
        }

        [data-testid="stChatMessage"] * {
            color: var(--text) !important;
        }

        /* ===== Tables / code ===== */
        table {
            border-radius: 12px;
            overflow: hidden;
        }

        pre {
            background: #141821 !important;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
        }

        /* ===== Scrollbar ===== */
        *::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        *::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.03);
        }

        *::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 999px;
        }

        *::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.18);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
