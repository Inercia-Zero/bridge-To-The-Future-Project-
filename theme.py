import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #212121;
            --bg-soft: #1b1b1b;
            --bg-elev: #171717;
            --panel: #262626;
            --panel-2: #2d2d2d;
            --panel-3: #343434;
            --border: rgba(255,255,255,0.08);
            --border-strong: rgba(255,255,255,0.14);
            --text: #f2f2f2;
            --muted: #b5b5b5;
            --soft: #8f8f8f;
            --accent: #6e8cff;
            --accent-soft: rgba(110, 140, 255, 0.14);
            --glow: 0 0 0 1px rgba(110, 140, 255, 0.10), 0 14px 36px rgba(0,0,0,0.34);
            --shadow: 0 12px 32px rgba(0,0,0,0.30);
            --radius: 22px;
            --radius-md: 16px;
            --radius-sm: 12px;
            --ui-font: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif;
        }

        /* esconder chrome do Streamlit */
        #MainMenu,
        header,
        footer,
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="collapsedControl"],
        .stDeployButton {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }

        html, body, .stApp {
            background:
                radial-gradient(circle at top left, rgba(90,110,170,0.10) 0%, rgba(90,110,170,0.00) 28%),
                radial-gradient(circle at top right, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.00) 24%),
                linear-gradient(180deg, #1f1f1f 0%, #181818 100%);
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
            color: var(--text);
        }

        /* manter matemática/código estáveis */
        .katex, .katex *, mjx-container, mjx-container *, code, pre, pre *, code * {
            font-family: inherit !important;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.1rem;
            padding-bottom: 1.2rem;
        }

        .chat-main-wrap {
            max-width: 980px;
            margin: 0 auto;
            padding-bottom: 0.8rem;
        }

        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at top, rgba(110,140,255,0.10) 0%, rgba(110,140,255,0.00) 26%),
                linear-gradient(180deg, #1d1d1d 0%, #171717 100%);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            color: var(--text) !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text) !important;
            letter-spacing: -0.03em;
            line-height: 1.05;
            font-weight: 780 !important;
        }

        p, li {
            line-height: 1.62;
        }

        .stCaption,
        .history-meta,
        .chat-topbar-meta {
            color: var(--muted) !important;
        }

        .chat-topbar {
            background:
                linear-gradient(180deg, rgba(44,44,44,0.96) 0%, rgba(35,35,35,0.96) 100%);
            border: 1px solid var(--border);
            border-radius: 28px;
            padding: 1.25rem 1.35rem;
            margin-bottom: 1.15rem;
            box-shadow: var(--glow);
            position: relative;
            overflow: hidden;
        }

        .chat-topbar::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, rgba(110,140,255,0.10), transparent 30%, transparent 70%, rgba(255,255,255,0.03));
            pointer-events: none;
        }

        .chat-topbar-title {
            position: relative;
            font-size: 1.45rem;
            font-weight: 800;
            color: #ffffff;
        }

        .chat-topbar-meta {
            position: relative;
            margin-top: 0.28rem;
            font-size: 0.98rem;
        }

        .context-chip {
            background: linear-gradient(180deg, rgba(43,43,43,0.96) 0%, rgba(34,34,34,0.96) 100%);
            border: 1px solid var(--border);
            color: var(--text);
            border-radius: 18px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.95rem;
            box-shadow: var(--shadow);
        }

        .history-card {
            background: linear-gradient(180deg, rgba(47,47,47,0.96) 0%, rgba(38,38,38,0.96) 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.62rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.20);
        }

        .history-card.active {
            border-color: rgba(110,140,255,0.34);
            box-shadow: var(--glow);
        }

        .history-title {
            font-weight: 760;
            font-size: 1.03rem;
            color: #ffffff;
        }

        .history-meta {
            margin-top: 0.2rem;
            font-size: 0.86rem;
        }

        div[data-testid="stExpander"] {
            background: linear-gradient(180deg, rgba(42,42,42,0.92) 0%, rgba(33,33,33,0.92) 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
        }

        .stTextInput input,
        .stTextArea textarea,
        [data-baseweb="input"] input,
        [data-baseweb="base-input"] input,
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {
            background: rgba(49,49,49,0.98) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
            min-height: 50px;
            box-shadow: none !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        [data-baseweb="input"] input:focus,
        .stSelectbox div[data-baseweb="select"] > div:focus-within,
        .stMultiSelect div[data-baseweb="select"] > div:focus-within {
            border-color: rgba(110,140,255,0.46) !important;
            box-shadow: 0 0 0 1px rgba(110,140,255,0.16) inset !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: var(--soft) !important;
        }

        .stButton > button,
        .stDownloadButton > button {
            background: linear-gradient(180deg, rgba(52,52,52,0.98) 0%, rgba(43,43,43,0.98) 100%);
            color: #f4f4f4;
            border: 1px solid var(--border);
            border-radius: 16px;
            min-height: 46px;
            font-weight: 680;
            letter-spacing: -0.01em;
            transition: 0.18s ease;
            box-shadow: 0 8px 18px rgba(0,0,0,0.18);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: rgba(110,140,255,0.28);
            background: linear-gradient(180deg, rgba(58,58,58,1) 0%, rgba(48,48,48,1) 100%);
            box-shadow: var(--glow);
            transform: translateY(-1px);
        }

        .stInfo, .stSuccess, .stWarning, .stError {
            border-radius: 16px;
            border-width: 1px;
        }

        [data-testid="stChatInput"] {
            background: transparent !important;
        }

        [data-testid="stChatInput"] > div {
            background: linear-gradient(180deg, rgba(43,43,43,0.98) 0%, rgba(33,33,33,0.98) 100%) !important;
            border: 1px solid rgba(110,140,255,0.14) !important;
            border-radius: 24px !important;
            box-shadow: var(--glow);
        }

        [data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: var(--text) !important;
            border: 0 !important;
            border-radius: 20px !important;
            min-height: 58px !important;
            font-size: 1rem !important;
            line-height: 1.5 !important;
        }

        [data-testid="stChatInputSubmitButton"] button,
        [data-testid="stChatInputSubmitButton"] {
            background: transparent !important;
        }

        [data-testid="stChatInputSubmitButton"] button {
            border-radius: 999px !important;
            background: linear-gradient(180deg, #5f7eff 0%, #4f6ee9 100%) !important;
            border: none !important;
            box-shadow: 0 8px 20px rgba(79,110,233,0.30) !important;
        }

        [data-testid="stChatInputSubmitButton"] button:hover {
            filter: brightness(1.06);
            transform: translateY(-1px);
        }

        a {
            color: #9bb2ff !important;
        }

        hr {
            border-color: var(--border);
        }

        /* refininho da tela inicial */
        .main .block-container > div:first-child h3,
        .main .block-container > div:first-child h2 {
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
