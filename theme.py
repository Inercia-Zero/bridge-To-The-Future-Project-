import streamlit as st

def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f6efe5;
            --bg-soft: #efe4d6;
            --sidebar: #eee2d0;
            --card: #fff9f2;
            --card-2: #fbf4ea;
            --line: #d9c7b2;
            --text: #2f261e;
            --muted: #6f6459;
            --accent: #8d725d;
            --accent-2: #6d5644;
            --success: #0f766e;
            --shadow: 0 10px 28px rgba(63, 44, 29, 0.08);
        }

        html, body, .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        section.main {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        header[data-testid="stHeader"] { background: transparent !important; }

        [data-testid="stSidebar"] {
            background: var(--sidebar) !important;
            border-right: 1px solid var(--line) !important;
        }

        [data-testid="stSidebar"] * { color: var(--text) !important; }

        .block-container {
            padding-top: 0.9rem !important;
            padding-bottom: 1rem !important;
            max-width: 1240px !important;
        }

        .brand-box, .hero-wrap, .mentor-card, .context-box, .materials-box, .landing-card, .history-card {
            background: var(--card);
            border: 1px solid var(--line);
            box-shadow: var(--shadow);
        }

        .brand-box { border-radius: 22px; padding: 14px; text-align: center; margin-bottom: 12px; }
        .brand-title { font-size: 1.05rem; font-weight: 900; margin-top: 4px; }
        .brand-sub { color: var(--muted); font-size: 0.9rem; }

        .hero-wrap {
            border-radius: 28px;
            padding: 26px 28px;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #fffaf3 0%, #f5ebdf 100%);
        }
        .hero-title { font-size: 2.1rem; line-height: 1.02; font-weight: 900; margin-bottom: 8px; }
        .hero-sub { color: var(--muted); font-size: 0.98rem; margin-bottom: 14px; }
        .mentor-highlight {
            background: rgba(255,255,255,0.7);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 16px 18px;
        }
        .mentor-highlight-title { font-size: 1.15rem; font-weight: 900; margin-bottom: 4px; }

        .mentor-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            margin: 0 0 18px 0;
        }
        .mentor-card { border-radius: 22px; padding: 16px; min-height: 156px; }
        .mentor-card.active { border: 2px solid var(--accent); background: #f7ede2; }
        .mentor-name { font-size: 1rem; font-weight: 900; margin-bottom: 6px; color: var(--text); }
        .mentor-desc { font-size: 0.92rem; line-height: 1.35; color: var(--muted); }

        .landing-wrap { max-width: 1100px; margin: 0 auto; padding-top: 0.6rem; }
        .landing-hero {
            border-radius: 30px;
            background: linear-gradient(135deg, #fffaf3 0%, #f0e2d3 100%);
            border: 1px solid var(--line);
            box-shadow: var(--shadow);
            padding: 30px;
            margin-bottom: 18px;
            text-align: center;
        }
        .landing-title { font-size: 2.4rem; font-weight: 900; line-height: 1; margin-bottom: 10px; }
        .landing-sub { color: var(--muted); font-size: 1rem; max-width: 760px; margin: 0 auto 18px auto; }
        .landing-card { border-radius: 24px; padding: 18px; margin-bottom: 10px; }
        .landing-emoji { font-size: 1.65rem; margin-bottom: 8px; }
        .landing-name { font-size: 1.05rem; font-weight: 900; margin-bottom: 6px; }
        .landing-desc { color: var(--muted); font-size: 0.92rem; min-height: 82px; }

        .history-card { border-radius: 16px; padding: 10px 12px; margin-bottom: 8px; background: var(--card-2); }
        .history-card.active { border: 2px solid var(--accent); background: #f3e6d8; }
        .history-title { font-size: 0.92rem; font-weight: 800; margin-bottom: 4px; }
        .history-meta { color: var(--muted); font-size: 0.78rem; }

        .chat-user, .chat-assistant {
            border-radius: 18px;
            padding: 0.95rem 1rem;
            border: 1px solid var(--line);
            box-shadow: var(--shadow);
            overflow-x: auto;
        }
        .chat-user { background: #fff4e7; }
        .chat-assistant { background: #ffffff; }

        .context-box, .materials-box { border-radius: 24px; padding: 18px; margin-bottom: 18px; }
        .materials-title { font-size: 1.1rem; font-weight: 900; margin-bottom: 6px; }
        .materials-sub, .small-muted { color: var(--muted) !important; }

        .stButton > button,
        div[data-testid="baseButton-secondary"] > button,
        div[data-testid="baseButton-primary"] > button {
            background: var(--accent) !important;
            color: #fffaf3 !important;
            border: 1px solid var(--accent) !important;
            border-radius: 14px !important;
            min-height: 42px !important;
            box-shadow: none !important;
        }
        .stButton > button:hover,
        div[data-testid="baseButton-secondary"] > button:hover,
        div[data-testid="baseButton-primary"] > button:hover {
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

        [data-testid="stChatInputContainer"],
        [data-testid="stBottomBlockContainer"] { background: transparent !important; }

        img { border-radius: 12px; }

        code { white-space: pre-wrap !important; }

        h1, h2, h3, h4, p, label, span, div { color: var(--text); }
        .stCaption { color: var(--muted) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
