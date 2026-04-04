import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #171717;
            --bg-2: #1f1f1f;
            --panel: #262626;
            --panel-2: #2e2e2e;
            --panel-3: #343434;
            --border: #3a3a3a;
            --text: #f3f4f6;
            --muted: #a1a1aa;
            --user: #303030;
            --assistant: #222222;
            --shadow: 0 10px 28px rgba(0, 0, 0, 0.28);
            --radius-xl: 24px;
            --radius-lg: 18px;
            --radius-md: 14px;
        }

        html, body, .stApp {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255,255,255,0.02), transparent 22%),
                linear-gradient(180deg, var(--bg) 0%, var(--bg-2) 100%) !important;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", sans-serif;
            color: var(--text);
        }

        h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: var(--text);
        }

        .small-muted {
            color: var(--muted) !important;
            font-size: 0.94rem;
            line-height: 1.5;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a1a 0%, #202020 100%) !important;
            border-right: 1px solid var(--border);
        }

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] > div,
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            background: var(--panel) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
            box-shadow: none !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        [data-testid="stChatInput"] textarea:focus,
        [data-testid="stChatInput"] input:focus {
            border-color: #525252 !important;
            box-shadow: none !important;
            outline: none !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #3a3a3a, #2b2b2b) !important;
            color: var(--text) !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
            font-weight: 600 !important;
            border: 1px solid #4a4a4a !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.20);
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            background: linear-gradient(135deg, #454545, #323232) !important;
            box-shadow: 0 10px 24px rgba(0,0,0,0.28);
        }

        div[role="radiogroup"] {
            gap: 0.45rem;
        }

        .sidebar-card,
        .history-card,
        .chat-header-card,
        .context-chip,
        .landing-card {
            background: var(--panel);
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
        }

        .sidebar-card {
            border-radius: var(--radius-lg);
            padding: 14px;
            margin-bottom: 16px;
        }

        .sidebar-title {
            font-size: 1.18rem;
            font-weight: 900;
            color: var(--text);
            margin-bottom: 6px;
        }

        .sidebar-sub {
            font-size: 0.92rem;
            color: var(--muted);
            line-height: 1.45;
        }

        .landing-wrap {
            max-width: 1120px;
            margin: 0 auto;
        }

        .landing-hero {
            background: linear-gradient(135deg, #262626 0%, #222222 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 28px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            text-align: center;
        }

        .landing-title {
            font-size: 2.3rem;
            font-weight: 900;
            color: var(--text);
            line-height: 1.08;
            margin-bottom: 10px;
            letter-spacing: -0.04em;
        }

        .landing-sub {
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.6;
            max-width: 760px;
            margin: 0 auto;
        }

        .landing-card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 14px;
            margin-bottom: 12px;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
            box-shadow: var(--shadow);
        }

        .landing-card:hover {
            transform: translateY(-4px);
            border-color: #525252;
            box-shadow: 0 18px 36px rgba(0,0,0,0.30);
        }

        .landing-card img {
            width: 100%;
            border-radius: 16px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.05);
            display: block;
            filter: brightness(0.94);
            box-shadow: 0 10px 22px rgba(0,0,0,0.22);
        }

        .landing-image-fallback {
            width: 100%;
            min-height: 180px;
            margin-bottom: 12px;
        }

        .landing-fallback-inner {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 180px;
            background: linear-gradient(135deg, #2a2a2a, #1d1d1d);
            border-radius: 16px;
            color: #d4d4d8;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 10px 22px rgba(0,0,0,0.22);
            font-weight: 800;
            letter-spacing: 0.08em;
            font-size: 2rem;
        }

        .landing-name {
            font-size: 1.14rem;
            font-weight: 800;
            color: var(--text) !important;
            margin-bottom: 6px;
            line-height: 1.3;
        }

        .landing-desc {
            color: var(--muted) !important;
            font-size: 0.96rem;
            line-height: 1.55;
        }

        [data-testid="stAlert"] {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
        }

        .history-card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 10px 12px;
            margin-bottom: 8px;
            box-shadow: var(--shadow);
        }

        .history-card.active {
            background: #313131 !important;
            border-color: #525252 !important;
        }

        .history-title {
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text);
            margin-bottom: 4px;
        }

        .history-meta {
            font-size: 0.76rem;
            color: var(--muted);
        }

        .chat-header-card {
            background: linear-gradient(135deg, #262626 0%, #222222 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 22px;
            margin-bottom: 14px;
            box-shadow: var(--shadow);
        }

        .chat-title {
            font-size: 2rem;
            font-weight: 900;
            line-height: 1.08;
            color: var(--text);
            margin-bottom: 6px;
            letter-spacing: -0.03em;
        }

        .chat-sub {
            color: var(--muted);
            font-size: 0.98rem;
            margin-bottom: 14px;
            line-height: 1.5;
        }

        .chat-mentor-box {
            background: var(--panel-2);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 14px;
        }

        .chat-mentor-title {
            font-size: 1.06rem;
            font-weight: 800;
            margin-bottom: 4px;
            color: var(--text);
        }

        .message-card {
            padding: 12px 16px;
            border-radius: 14px;
            margin-bottom: 10px;
            max-width: 75%;
            border: 1px solid var(--border);
            box-shadow: 0 6px 16px rgba(0,0,0,0.18);
            line-height: 1.65;
            font-size: 0.98rem;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .message-user {
            background: var(--user) !important;
            color: var(--text) !important;
            margin-left: auto;
        }

        .message-assistant {
            background: var(--assistant) !important;
            color: var(--text) !important;
            margin-right: auto;
        }

        .context-chip {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 12px 14px;
            margin-bottom: 14px;
            color: var(--text);
            box-shadow: var(--shadow);
        }

        .streamlit-expanderHeader {
            background: var(--panel) !important;
            border-radius: 12px !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
        }

        [data-testid="stFileUploader"] {
            background: var(--panel);
            border: 1px dashed rgba(255,255,255,0.12);
            border-radius: 16px;
            padding: 10px;
        }

        [data-testid="stImage"] img {
            border-radius: 18px;
        }

        [data-testid="stChatInput"] {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        [data-testid="stChatInput"] > div {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        a {
            color: #d4d4d8 !important;
        }

        hr {
            border-color: var(--border) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
