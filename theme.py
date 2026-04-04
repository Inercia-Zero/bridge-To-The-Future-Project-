import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #212121;
            --bg-soft: #262626;
            --panel: #2a2a2a;
            --panel-2: #303030;
            --panel-3: #383838;
            --border: #3a3a3a;
            --text: #ececec;
            --muted: #b8b8b8;
            --accent: #a67c52;
            --accent-hover: #b58963;
            --user: #2f2a26;
            --assistant: #2a2a2a;
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
                radial-gradient(circle at top left, rgba(255,255,255,0.025), transparent 20%),
                linear-gradient(180deg, #212121 0%, #1c1c1c 100%) !important;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1.2rem;
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

        /* Streamlit base */
        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e1e1e 0%, #232323 100%) !important;
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
            border-color: rgba(166,124,82,0.5) !important;
            box-shadow: 0 0 0 1px rgba(166,124,82,0.18) !important;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 14px !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            background: linear-gradient(180deg, var(--accent) 0%, #8f6745 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 0.64rem 1rem !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.24);
            transition: all 0.18s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(180deg, var(--accent-hover) 0%, #9a724f 100%) !important;
            transform: translateY(-1px);
            box-shadow: 0 12px 26px rgba(0,0,0,0.30);
        }

        /* Radio */
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
            font-size: 1.2rem;
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
            background: linear-gradient(135deg, #2a2a2a 0%, #242424 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 28px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            text-align: center;
        }

        .landing-title {
            font-size: 2.4rem;
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
            border-color: rgba(166,124,82,0.35);
            box-shadow: 0 18px 36px rgba(0,0,0,0.30);
        }

        .landing-card img {
            width: 100%;
            border-radius: 16px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.06);
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

        .landing-emoji {
            font-size: 2.4rem;
            margin-bottom: 10px;
        }

        .landing-name {
            font-size: 1.16rem;
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

        /* Info / success boxes from Streamlit */
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
            background: #332a24 !important;
            border-color: rgba(166,124,82,0.35) !important;
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
            background: linear-gradient(135deg, #2b2b2b 0%, #242424 100%);
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

        /* Markdown links / misc */
        a {
            color: #d2ab82 !important;
        }

        /* Hide weird bright separators if any */
        hr {
            border-color: var(--border) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
