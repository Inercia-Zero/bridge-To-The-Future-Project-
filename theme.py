import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #212121;
            --bg-2: #1b1b1b;
            --panel: #2a2a2a;
            --panel-2: #303030;
            --panel-3: #383838;
            --border: #3a3a3a;
            --text: #ececec;
            --muted: #b3b3b3;
            --accent: #a67c52;
            --accent-hover: #b58963;
            --accent-soft: rgba(166,124,82,0.16);
            --user: #2f2924;
            --assistant: #2a2a2a;
            --shadow: 0 10px 28px rgba(0, 0, 0, 0.24);
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
            background: linear-gradient(180deg, #1f1f1f 0%, #252525 100%) !important;
            border-right: 1px solid var(--border);
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
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        [data-testid="stChatInput"] textarea:focus,
        [data-testid="stChatInput"] input:focus {
            border-color: rgba(166,124,82,0.55) !important;
            box-shadow: 0 0 0 1px rgba(166,124,82,0.18) !important;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 14px !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            background: #3a312a !important;
            color: var(--text) !important;
            font-weight: 700 !important;
            padding: 0.64rem 1rem !important;
            box-shadow: 0 6px 16px rgba(0,0,0,0.20);
            transition: all 0.18s ease;
        }

        .stButton > button:hover {
            background: #46382d !important;
            border-color: rgba(166,124,82,0.28) !important;
            transform: translateY(-1px);
        }

        /* Primary accent buttons look a bit warmer when focused/active */
        .stButton > button:focus,
        .stButton > button:active {
            box-shadow: 0 0 0 1px rgba(166,124,82,0.18) !important;
        }

        div[role="radiogroup"] {
            gap: 0.45rem;
        }

        /* Generic cards */
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

        /* Landing */
        .landing-wrap {
            max-width: 1120px;
            margin: 0 auto;
        }

        .landing-hero {
            background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
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
            border-radius: var(--radius-lg);
            padding: 14px;
            margin-bottom: 12px;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .landing-card:hover {
            transform: translateY(-4px);
            border-color: rgba(166,124,82,0.34);
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
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            background: var(--panel-2);
            border: 1px dashed rgba(255,255,255,0.10);
            margin-bottom: 12px;
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

        /* Alerts */
        [data-testid="stAlert"] {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
        }

        /* History */
        .history-card {
            border-radius: 14px;
            padding: 10px 12px;
            margin-bottom: 8px;
        }

        .history-card.active {
            background: #332b25 !important;
            border-color: rgba(166,124,82,0.32) !important;
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

        /* Chat header */
        .chat-header-card {
            background: linear-gradient(135deg, #2a2a2a 0%, #242424 100%);
            border-radius: var(--radius-xl);
            padding: 22px;
            margin-bottom: 14px;
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

        /* Messages */
        .message-card {
            border-radius: 18px;
            padding: 14px 16px;
            margin-bottom: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 6px 16px rgba(0,0,0,0.18);
            line-height: 1.65;
            font-size: 0.98rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: var(--text) !important;
        }

        .message-user {
            background: var(--user) !important;
        }

        .message-assistant {
            background: var(--assistant) !important;
        }

        /* Context chip */
        .context-chip {
            border-radius: 14px;
            padding: 12px 14px;
            margin-bottom: 14px;
            color: var(--text);
        }

        /* Expander */
        .streamlit-expanderHeader {
            background: var(--panel) !important;
            border-radius: 12px !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
        }

        /* File uploader */
        [data-testid="stFileUploader"] {
            background: var(--panel);
            border: 1px dashed rgba(255,255,255,0.12);
            border-radius: 16px;
            padding: 10px;
        }

        /* Images */
        [data-testid="stImage"] img {
            border-radius: 18px;
        }

        a {
            color: #d2ab82 !important;
        }

        hr {
            border-color: var(--border) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
