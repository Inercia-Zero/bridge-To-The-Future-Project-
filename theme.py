import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #f7f1e8 0%, #f3eadf 100%);
        color: #2b2b2b;
    }

    [data-testid="stSidebar"] {
        background-color: #efe4d6;
        border-right: 1px solid rgba(120, 90, 60, 0.12);
    }

    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.55);
        border: 1px solid rgba(120, 90, 60, 0.10);
        border-radius: 16px;
        padding: 0.5rem;
    }

    .stButton > button {
        background-color: #e8d8c3;
        color: #2b2b2b;
        border: none;
        border-radius: 12px;
    }

    .stButton > button:hover {
        background-color: #dcc7ac;
        color: #1f1f1f;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #fffaf5;
        color: #2b2b2b;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
