import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #181818;
            --panel: #232323;
            --panel-2: #2b2b2b;
            --border: #353535;
            --text: #f5f5f5;
            --muted: #b3b3b3;
            --user-bg: #2f2f2f;
            --assistant-bg: #222222;
        }

        html, body, .stApp {
            background: var(--bg) !important;
            color: var(--text) !important;
            font-family: "Inter", sans-serif !important;
        }

        [data-testid="stAppViewContainer"] {
            background: var(--bg) !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }

        section[data-testid="stSidebar"] {
            background: #1d1d1d !important;
            border-right: 1px solid #2e2e2e !important;
        }

        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: var(--text) !important;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] > div,
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            background: var(--panel) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
        }

        .stButton > button {
            background: var(--panel) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }

        .stButton > button:hover {
            background: var(--panel-2) !important;
            border-color: #4a4a4a !important;
        }

        .sidebar-card,
        .history-card,
        .landing-card,
        .context-chip {
            background: var(--panel) !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
            padding: 12px !important;
            margin-bottom: 10px !important;
        }

        .sidebar-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text);
        }

        .sidebar-sub,
        .history-meta,
        .small-muted {
            color: var(--muted) !important;
        }

        .history-title,
        .landing-name {
            font-weight: 700;
            color: var(--text) !important;
        }

        .landing-desc {
            color: var(--muted) !important;
        }

        .chat-main-wrap {
            max-width: 860px;
            margin: 0 auto;
        }

        .chat-sticky-top {
            position: sticky;
            top: 0;
            z-index: 20;
            background: rgba(24,24,24,0.92);
            backdrop-filter: blur(10px);
            padding: 12px 8px 10px 8px;
            border-bottom: 1px solid #2c2c2c;
            margin-bottom: 14px;
        }

        .chat-sticky-master {
            font-size: 1.25rem;
            font-weight: 800;
            text-align: center;
            color: var(--text);
        }

        .chat-sticky-professor {
            font-size: 0.95rem;
            text-align: center;
            color: var(--muted);
            margin-top: 2px;
        }

        .msg-row {
            display: flex;
            width: 100%;
            margin: 10px 0;
        }

        .msg-row-user {
            justify-content: flex-end;
        }

        .msg-row-assistant {
            justify-content: flex-start;
        }

        .msg-bubble {
            max-width: 78%;
            padding: 12px 14px;
            border-radius: 18px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 14px rgba(0,0,0,0.18);
        }

        .msg-bubble-user {
            background: var(--user-bg);
            border-bottom-right-radius: 6px;
        }

        .msg-bubble-assistant {
            background: var(--assistant-bg);
            border-bottom-left-radius: 6px;
        }

        .msg-meta {
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--muted);
            margin-bottom: 6px;
        }

        .msg-content {
            color: var(--text);
            line-height: 1.65;
            word-break: break-word;
        }

        .msg-attachment {
            margin-top: 8px;
            font-size: 0.82rem;
            color: var(--muted);
            padding: 6px 8px;
            background: rgba(255,255,255,0.04);
            border-radius: 10px;
        }

        .context-chip {
            color: var(--text) !important;
        }

        [data-testid="stImage"] img {
            border-radius: 14px !important;
        }

        [data-testid="stFileUploader"] {
            background: var(--panel) !important;
            border: 1px dashed var(--border) !important;
            border-radius: 14px !important;
            padding: 8px !important;
        }

        #MainMenu, footer, header,
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
