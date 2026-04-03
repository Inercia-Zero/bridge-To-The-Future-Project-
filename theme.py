import streamlit as st

def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f6efe5;
            --bg-soft: #efe4d6;
            --sidebar: #f1e7da;
            --card: #fff9f2;
            --card-2: #fcf5eb;
            --line: #d9c7b2;
            --text: #2f261e;
            --muted: #6f6459;
            --accent: #8d725d;
            --accent-2: #6d5644;
            --green: #0f766e;
            --shadow: 0 10px 30px rgba(63, 44, 29, 0.08);
        }

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stMain"] {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        [data-testid="stSidebar"] {
            background: var(--sidebar) !important;
            border-right: 1px solid var(--line) !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--text) !important;
        }

        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            max-width: 1250px !important;
        }

        .hero-wrap {
            background: linear-gradient(135deg, #fffaf3 0%, #f5ebdf 100%);
            border: 1px solid var(--line);
            border-radius: 28px;
            padding: 26px 28px;
            box-shadow: var(--shadow);
            margin-bottom: 16px;
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 900;
            line-height: 1.05;
            color: var(--text);
            margin-bottom: 6px;
        }

        .hero-sub {
            color: var(--muted);
            font-size: 0.98rem;
            margin-bottom: 18px;
        }

        .mentor-highlight {
            padding: 16px 18px;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.65);
            margin-top: 8px;
        }

        .mentor-highlight-title {
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .mentor-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            margin: 14px 0 18px 0;
        }

        .mentor-card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 16px;
            box-shadow: var(--shadow);
            min-height: 150px;
        }

        .mentor-card.active {
            border: 2px solid var(--accent);
            background: #f7ede2;
        }

        .mentor-name {
            font-size: 1.05rem;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .mentor-desc {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.35;
        }

        .brand-box {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 14px;
            box-shadow: var(--shadow);
            margin-bottom: 12px;
            text-align: center;
        }

        .brand-title {
            font-weight: 900;
            font-size: 1.1rem;
            margin-bottom: 4px;
        }

        .brand-sub {
            color: var(--muted);
            font-size: 0.9rem;
        }

        .chat-user,
        .chat-assistant {
            border-radius: 18px;
            padding: 0.9rem 1rem;
            border: 1px solid var(--line);
            box-shadow: var(--shadow);
            overflow-x: auto;
        }

        .chat-user {
            background: #fff6ea;
        }

        .chat-assistant {
            background: #ffffff;
        }

        .context-box,
        .materials-box {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 18px;
            box-shadow: var(--shadow);
            margin-bottom: 18px;
        }

        .materials-title {
            font-size: 1.15rem;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .materials-sub {
            color: var(--muted);
            margin-bottom: 12px;
        }

        .stButton > button {
            background: var(--accent) !important;
            color: white !important;
            border: 1px solid var(--accent) !important;
            border-radius: 14px !important;
            min-height: 42px !important;
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

        code {
            white-space: pre-wrap !important;
        }

        .stCaption, .small-muted {
            color: var(--muted) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
