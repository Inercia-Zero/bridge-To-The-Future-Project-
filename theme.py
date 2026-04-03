
import streamlit as st

def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f6efe5;
            --sidebar: #eee2d0;
            --card: #fff9f2;
            --card-soft: #fbf4ea;
            --line: #d9c7b2;
            --text: #2f261e;
            --muted: #6f6459;
            --accent: #8d725d;
            --accent-2: #6d5644;
            --shadow: 0 10px 28px rgba(63, 44, 29, 0.08);
        }

        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 1280px !important;
            padding-top: 0.8rem !important;
            padding-bottom: 0.8rem !important;
        }

        .sidebar-card, .chat-header-card, .landing-card, .landing-hero, .message-card, .context-chip, .history-card, .materials-card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 22px;
            box-shadow: var(--shadow);
        }

        .sidebar-card {
            padding: 14px;
            margin-bottom: 12px;
            text-align: center;
            background: var(--sidebar);
        }

        .sidebar-title {
            font-weight: 900;
            font-size: 1.05rem;
            margin-top: 4px;
        }

        .sidebar-sub {
            font-size: 0.88rem;
            color: var(--muted);
        }

        .chat-header-card {
            padding: 22px;
            margin-bottom: 14px;
            background: linear-gradient(135deg, #fffaf3 0%, #f3e5d6 100%);
        }

        .chat-title {
            font-size: 2rem;
            font-weight: 900;
            line-height: 1.02;
            margin-bottom: 8px;
        }

        .chat-sub {
            color: var(--muted);
            margin-bottom: 14px;
        }

        .chat-mentor-box {
            background: rgba(255,255,255,0.72);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 14px 16px;
        }

        .chat-mentor-title {
            font-size: 1.08rem;
            font-weight: 900;
            margin-bottom: 4px;
        }

        .landing-wrap {
            max-width: 1120px;
            margin: 0 auto;
            padding-top: 0.5rem;
        }

        .landing-hero {
            padding: 28px;
            text-align: center;
            margin-bottom: 18px;
            background: linear-gradient(135deg, #fffaf3 0%, #f0e2d3 100%);
        }

        .landing-title {
            font-size: 2.3rem;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 10px;
        }

        .landing-sub {
            color: var(--muted);
            max-width: 760px;
            margin: 0 auto 16px auto;
        }

        .landing-card {
            padding: 18px;
            margin-bottom: 12px;
            min-height: 170px;
        }

        .landing-emoji {
            font-size: 1.6rem;
            margin-bottom: 8px;
        }

        .landing-name {
            font-size: 1.05rem;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .landing-desc {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.35;
            min-height: 78px;
        }

        .history-card {
            padding: 10px 12px;
            margin-bottom: 8px;
            background: var(--card-soft);
            border-radius: 16px;
            box-shadow: none;
        }

        .history-card.active {
            border: 2px solid var(--accent);
            background: #f3e6d8;
        }

        .history-title {
            font-size: 0.92rem;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .history-meta {
            color: var(--muted);
            font-size: 0.78rem;
        }

        .message-card {
            padding: 0.95rem 1rem;
            margin-bottom: 10px;
            overflow-x: auto;
        }

        .message-user {
            background: #fff4e7;
        }

        .message-assistant {
            background: #ffffff;
        }

        .context-chip {
            padding: 12px 14px;
            margin-bottom: 14px;
            border-radius: 18px;
        }

        .mentor-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            margin: 0 0 14px 0;
        }

        .mini-mentor {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 14px;
        }

        .mini-mentor.active {
            border: 2px solid var(--accent);
            background: #f7ede2;
        }

        .mini-mentor-name {
            font-weight: 900;
            margin-bottom: 6px;
        }

        .mini-mentor-desc {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.3;
        }

        .materials-card {
            padding: 18px;
            margin-bottom: 18px;
        }

        .stButton > button {
            background: var(--accent) !important;
            color: #fffaf3 !important;
            border: 1px solid var(--accent) !important;
            border-radius: 14px !important;
            min-height: 40px !important;
            box-shadow: none !important;
        }

        .stButton > button:hover {
            background: var(--accent-2) !important;
            border-color: var(--accent-2) !important;
        }

        .stSelectbox div[data-baseweb="select"] > div,
        .stTextInput input,
        .stTextArea textarea,
        [data-testid="stChatInput"] textarea,
        .stFileUploader section,
        .stRadio > div {
            background: #fff9f3 !important;
            color: var(--text) !important;
            border: 1px solid var(--line) !important;
            border-radius: 14px !important;
        }

        [data-testid="stChatMessageContent"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        .stCaption {
            color: var(--muted) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
