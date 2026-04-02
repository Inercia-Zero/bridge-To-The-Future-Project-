import streamlit as st

def apply_theme() -> None:
    st.markdown(
        '''
        <style>
        :root {
            --bg: #f6f0e6;
            --card: #fffaf3;
            --line: #d9c8b4;
            --text: #2d241c;
            --muted: #6f6257;
            --accent: #8a735f;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stSidebar"] {
            background: var(--bg);
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--line);
        }

        [data-testid="stChatMessageContent"] {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 0.8rem 1rem;
        }

        .stSelectbox div[data-baseweb="select"] > div,
        .stTextInput input,
        .stTextArea textarea,
        [data-testid="stChatInput"] textarea {
            background: var(--card) !important;
            color: var(--text) !important;
            border: 1px solid var(--line) !important;
            border-radius: 14px !important;
        }

        .stButton > button {
            background: var(--accent) !important;
            color: white !important;
            border-radius: 12px !important;
            border: 1px solid var(--accent) !important;
        }

        h1, h2, h3, p, label, span, div {
            color: var(--text);
        }

        .stCaption {
            color: var(--muted) !important;
        }
        </style>
        ''',
        unsafe_allow_html=True,
    )
