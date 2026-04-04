import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #171717;
            --bg-2: #1d1d1d;
            --panel: #222222;
            --panel-2: #282828;
            --panel-3: #303030;
            --border: #343434;
            --border-soft: #2b2b2b;
            --text: #f5f5f5;
            --muted: #a3a3a3;
            --muted-2: #8a8a8a;
            --user: #2f2f2f;
            --assistant: #1f1f1f;
            --shadow: 0 10px 30px rgba(0, 0, 0, 0.26);
            --radius-xl: 24px;
            --radius-lg: 18px;
            --radius-md: 14px;
            --radius-sm: 12px;
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

        h1, h2, h3, h4, h5, h6 {
            color: var(--text) !important;
            letter-spacing: -0.02em;
        }

        p, div, span, label {
            color: var(--text);
        }

        .small-muted {
            color: var(--muted) !important;
            font-size: 0.94rem;
            line-height: 1.55;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #181818 0%, #1d1d1d 100%) !important;
            border-right: 1px solid var(--border-soft);
        }

        /* Inputs */
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
            border-color: #4a4a4a !important;
            box-shadow: none !important;
            outline: none !important;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(180deg, #343434, #2a2a2a) !important;
            color: var(--text) !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
            font-weight: 600 !important;
            border: 1px solid #424242 !important;
            transition: all 0.18s ease !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            background: linear-gradient(180deg, #3a3a3a, #303030) !important;
            border-color: #555555 !important;
            box-shadow: 0 12px 24px rgba(0,0,0,0.24);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        div[role="radiogroup"] {
            gap: 0.45rem;
        }

        /* Shared panels */
        .sidebar-card,
        .history-card,
        .chat-header-card,
        .context-chip,
        .landing-card {
            background: var(--panel);
            border: 1px solid var(--border-soft);
            box-shadow: var(--shadow);
        }

        /* Sidebar */
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

        /* Landing */
        .landing-wrap {
            max-width: 1120px;
            margin: 0 auto;
        }

        .landing-hero {
            background: linear-gradient(180deg, #222222 0%, #1d1d1d 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 26px 28px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            text-align: center;
        }

        .landing-title {
            font-size: 2.25rem;
            font-weight: 900;
            color: var(--text);
            line-height: 1.08;
            margin-bottom: 10px;
            letter-spacing: -0.04em;
        }

        .landing-sub {
            color: var(--muted);
            font-size: 0.98rem;
            line-height: 1.65;
            max-width: 760px;
            margin: 0 auto;
        }

        .landing-card {
            background: linear-gradient(180deg, #222222 0%, #1d1d1d 100%);
            border: 1px solid var(--border-soft);
            border-radius: var(--radius-lg);
            padding: 14px;
            margin-bottom: 12px;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
            box-shadow: var(--shadow);
        }

        .landing-card:hover {
            transform: translateY(-3px);
            border-color: #4a4a4a;
            box-shadow: 0 18px 36px rgba(0,0,0,0.28);
        }

        .landing-card img {
            width: 100%;
            border-radius: 16px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.04);
            display: block;
            filter: brightness(0.95);
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
            background: linear-gradient(180deg, #2a2a2a, #202020);
            border-radius: 16px;
            color: #d4d4d8;
            border: 1px solid rgba(255,255,255,0.05);
            box-shadow: 0 10px 22px rgba(0,0,0,0.22);
            font-weight: 800;
            letter-spacing: 0.08em;
            font-size: 2rem;
        }

        .landing-name {
            font-size: 1.12rem;
            font-weight: 800;
            color: var(--text) !important;
            margin-bottom: 6px;
            line-height: 1.3;
        }

        .landing-desc {
            color: var(--muted) !important;
            font-size: 0.95rem;
            line-height: 1.55;
        }

        /* Alerts */
        [data-testid="stAlert"] {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
        }

        /* History */
        .history-card {
            background: linear-gradient(180deg, #242424 0%, #1f1f1f 100%);
            border: 1px solid var(--border-soft);
            border-radius: 14px;
            padding: 11px 12px;
            margin-bottom: 8px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        }

        .history-card.active {
            background: linear-gradient(180deg, #2d2d2d 0%, #252525 100%) !important;
            border-color: #4d4d4d !important;
        }

        .history-title {
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text);
            margin-bottom: 4px;
        }

        .history-meta {
            font-size: 0.76rem;
            color: var(--muted-2);
        }

        /* Chat header */
        .chat-header-card {
            background: linear-gradient(180deg, #232323 0%, #1d1d1d 100%);
            border: 1px solid var(--border-soft);
            border-radius: var(--radius-xl);
            padding: 22px;
            margin-bottom: 16px;
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
            background: #282828;
            border: 1px solid var(--border-soft);
            border-radius: 16px;
            padding: 14px;
        }

        .chat-mentor-title {
            font-size: 1.06rem;
            font-weight: 800;
            margin-bottom: 4px;
            color: var(--text);
        }

        /* Messages */
        .message-card {
            padding: 14px 18px;
            border-radius: 16px;
            margin-bottom: 12px;
            max-width: 74%;
            border: 1px solid var(--border-soft);
            box-shadow: 0 6px 16px rgba(0,0,0,0.16);
            line-height: 1.7;
            font-size: 0.98rem;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .message-user {
            background: #303030 !important;
            color: var(--text) !important;
            margin-left: auto;
            border-radius: 16px 16px 6px 16px;
        }

        .message-assistant {
            background: #1f1f1f !important;
            color: var(--text) !important;
            margin-right: auto;
            border-radius: 16px 16px 16px 6px;
        }

        /* Context chip */
        .context-chip {
            background: #232323;
            border: 1px solid var(--border-soft);
            border-radius: 14px;
            padding: 12px 14px;
            margin-bottom: 14px;
            color: var(--text);
            box-shadow: 0 8px 18px rgba(0,0,0,0.16);
        }

        /* Expander */
        .streamlit-expanderHeader {
            background: var(--panel) !important;
            border-radius: 12px !important;
            color: var(--text) !important;
            border: 1px solid var(--border-soft) !important;
        }

        /* Upload */
        [data-testid="stFileUploader"] {
            background: var(--panel);
            border: 1px dashed rgba(255,255,255,0.10);
            border-radius: 16px;
            padding: 10px;
        }

        /* Images */
        [data-testid="stImage"] img {
            border-radius: 18px;
        }

        /* Chat input */
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

        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            background: #222222 !important;
            border: 1px solid #333333 !important;
            border-radius: 18px !important;
            color: var(--text) !important;
            box-shadow: none !important;
        }

        [data-testid="stChatInput"] textarea:focus,
        [data-testid="stChatInput"] input:focus {
            border: 1px solid #4a4a4a !important;
            box-shadow: none !important;
            outline: none !important;
        }

        a {
            color: #d4d4d8 !important;
        }

        hr {
            border-color: var(--border) !important;
        }

        /* Remove Streamlit UI */
        #MainMenu {
            display: none !important;
        }

        [data-testid="stStatusWidget"] {
            display: none !important;
        }

        header {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        [data-testid="stDecoration"] {
            display: none !important;
        }

        footer {
            display: none !important;
        }

        button[kind="header"] {
            display: none !important;
        }

        div[data-testid="stToolbar"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
