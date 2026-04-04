import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #f5efe6;
            --panel: rgba(255, 255, 255, 0.72);
            --panel-strong: rgba(255, 250, 243, 0.96);
            --border: rgba(120, 90, 60, 0.16);
            --text: #3d2f24;
            --muted: #7b6758;
            --accent: #a67c52;
            --accent-2: #8d6b49;
            --user: #efe3d3;
            --assistant: #ffffff;
            --shadow: 0 10px 30px rgba(80, 55, 30, 0.08);
            --radius-xl: 24px;
            --radius-lg: 18px;
            --radius-md: 14px;
        }

        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255,255,255,0.65), transparent 30%),
                linear-gradient(180deg, #f9f3ea 0%, #f3eadf 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }

        /* ========= TEXTOS GERAIS ========= */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text);
            letter-spacing: -0.02em;
        }

        p, li, div, span, label {
            color: var(--text);
        }

        .small-muted {
            color: var(--muted);
            font-size: 0.94rem;
            line-height: 1.5;
        }

        /* ========= INPUTS ========= */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] > div,
        .stNumberInput input {
            background: rgba(255,255,255,0.82) !important;
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
            color: var(--text) !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: rgba(166,124,82,0.4) !important;
            box-shadow: 0 0 0 1px rgba(166,124,82,0.18) !important;
        }

        /* ========= BOTÕES ========= */
        .stButton > button {
            border-radius: 14px !important;
            border: 1px solid rgba(120,90,60,0.14) !important;
            background: linear-gradient(180deg, #a98763 0%, #967251 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 0.62rem 1rem !important;
            box-shadow: 0 6px 18px rgba(120, 90, 60, 0.12);
            transition: all 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            filter: brightness(1.03);
            box-shadow: 0 10px 24px rgba(120,90,60,0.16);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* ========= RADIO ========= */
        div[role="radiogroup"] {
            gap: 0.4rem;
        }

        /* ========= LANDING ========= */
        .landing-wrap {
            max-width: 1120px;
            margin: 0 auto;
        }

        .landing-hero {
            background: linear-gradient(135deg, rgba(255,250,243,0.96) 0%, rgba(236,221,204,0.9) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 28px 28px;
            margin-bottom: 18px;
            box-shadow: var(--shadow);
            text-align: center;
        }

        .landing-title {
            font-size: 2.4rem;
            font-weight: 900;
            color: var(--text);
            line-height: 1.1;
            margin-bottom: 10px;
            letter-spacing: -0.04em;
        }

        .landing-sub {
            font-size: 1rem;
            color: var(--muted);
            max-width: 760px;
            margin: 0 auto;
            line-height: 1.6;
        }

        .landing-card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 16px;
            box-shadow: var(--shadow);
            margin-bottom: 12px;
            min-height: 100%;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .landing-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 32px rgba(80, 55, 30, 0.12);
        }

        .landing-card img {
            width: 100%;
            border-radius: 18px;
            margin-bottom: 12px;
            border: 1px solid rgba(120,90,60,0.10);
            box-shadow: 0 8px 20px rgba(40, 25, 15, 0.08);
        }

        .landing-image-fallback {
            width: 100%;
            min-height: 180px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            background: rgba(255,255,255,0.55);
            border: 1px dashed rgba(120,90,60,0.18);
            margin-bottom: 12px;
        }

        .landing-emoji {
            font-size: 2.6rem;
            margin-bottom: 10px;
        }

        .landing-name {
            font-size: 1.24rem;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 6px;
            line-height: 1.25;
        }

        .landing-desc {
            color: var(--muted);
            font-size: 0.98rem;
            line-height: 1.55;
        }

        /* ========= SIDEBAR ========= */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255,249,242,0.98) 0%, rgba(242,232,219,0.96) 100%);
            border-right: 1px solid rgba(120,90,60,0.08);
        }

        .sidebar-card {
            background: rgba(255,255,255,0.45);
            border: 1px solid rgba(120,90,60,0.12);
            border-radius: 18px;
            padding: 14px;
            margin-bottom: 16px;
        }

        .sidebar-title {
            font-size: 1.2rem;
            font-weight: 900;
            color: var(--text);
            line-height: 1.1;
            margin-bottom: 6px;
        }

        .sidebar-sub {
            font-size: 0.92rem;
            color: var(--muted);
            line-height: 1.45;
        }

        .history-card {
            background: rgba(255,255,255,0.62);
            border: 1px solid rgba(120,90,60,0.12);
            border-radius: 14px;
            padding: 10px 12px;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px rgba(80,55,30,0.05);
        }

        .history-card.active {
            background: rgba(166,124,82,0.16);
            border-color: rgba(166,124,82,0.28);
        }

        .history-title {
            font-weight: 700;
            font-size: 0.95rem;
            line-height: 1.3;
            color: var(--text);
            margin-bottom: 4px;
        }

        .history-meta {
            font-size: 0.76rem;
            color: var(--muted);
        }

        /* ========= HEADER DO CHAT ========= */
        .chat-header-card {
            background: linear-gradient(135deg, rgba(255,250,243,0.97) 0%, rgba(238,225,210,0.92) 100%);
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
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(120,90,60,0.10);
            border-radius: 16px;
            padding: 14px;
        }

        .chat-mentor-title {
            font-size: 1.06rem;
            font-weight: 800;
            margin-bottom: 4px;
            color: var(--text);
        }

        /* ========= MENSAGENS ========= */
        .message-card {
            border-radius: 18px;
            padding: 14px 16px;
            margin-bottom: 12px;
            border: 1px solid rgba(120,90,60,0.10);
            box-shadow: 0 6px 18px rgba(80,55,30,0.06);
            line-height: 1.65;
            font-size: 0.98rem;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .message-user {
            background: var(--user);
        }

        .message-assistant {
            background: var(--assistant);
        }

        /* ========= CHIPS / CONTEXTO ========= */
        .context-chip {
            background: rgba(255,255,255,0.68);
            border: 1px solid rgba(120,90,60,0.14);
            border-radius: 14px;
            padding: 12px 14px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(80,55,30,0.05);
            color: var(--text);
        }

        /* ========= EXPANDER ========= */
        .streamlit-expanderHeader {
            background: rgba(255,255,255,0.45);
            border-radius: 12px;
        }

        /* ========= FILE UPLOADER ========= */
        [data-testid="stFileUploader"] {
            background: rgba(255,255,255,0.55);
            border: 1px dashed rgba(120,90,60,0.22);
            border-radius: 16px;
            padding: 10px;
        }

        /* ========= CHAT INPUT ========= */
        [data-testid="stChatInput"] {
            margin-top: 10px;
        }

        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            background: rgba(255,255,255,0.85) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(120,90,60,0.14) !important;
        }

        /* ========= IMAGENS DENTRO DO CHAT ========= */
        [data-testid="stImage"] img {
            border-radius: 18px;
        }

        /* ========= TEMA ESCURO CONTROLADO ========= */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #141414;
                --panel: rgba(32, 32, 32, 0.88);
                --panel-strong: rgba(24, 24, 24, 0.96);
                --border: rgba(255,255,255,0.08);
                --text: #f5f0ea;
                --muted: #c5b8a9;
                --accent: #c49a6c;
                --accent-2: #ad8359;
                --user: #2a211b;
                --assistant: #1f1b18;
                --shadow: 0 10px 26px rgba(0,0,0,0.28);
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(255,255,255,0.03), transparent 26%),
                    linear-gradient(180deg, #141414 0%, #1b1816 100%);
                color: var(--text);
            }

            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, rgba(22,22,22,0.96) 0%, rgba(28,24,22,0.96) 100%);
                border-right: 1px solid rgba(255,255,255,0.05);
            }

            .landing-hero,
            .chat-header-card,
            .sidebar-card,
            .landing-card,
            .history-card,
            .context-chip,
            .message-card,
            .chat-mentor-box {
                background: rgba(26, 23, 21, 0.92) !important;
                color: var(--text) !important;
                border-color: rgba(255,255,255,0.08) !important;
            }

            .landing-sub,
            .landing-desc,
            .chat-sub,
            .sidebar-sub,
            .history-meta,
            .small-muted {
                color: var(--muted) !important;
            }

            .landing-image-fallback {
                background: rgba(255,255,255,0.04);
                border: 1px dashed rgba(255,255,255,0.10);
            }

            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox div[data-baseweb="select"] > div,
            .stNumberInput input,
            [data-testid="stChatInput"] textarea,
            [data-testid="stChatInput"] input {
                background: rgba(28,28,28,0.95) !important;
                color: var(--text) !important;
                border-color: rgba(255,255,255,0.08) !important;
            }

            .stButton > button {
                background: linear-gradient(180deg, #b58963 0%, #986f4d 100%) !important;
                border-color: rgba(255,255,255,0.05) !important;
            }

            .message-user {
                background: #2a211b !important;
            }

            .message-assistant {
                background: #1c1917 !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
