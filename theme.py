import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background: #f4efe6;
            color: #2b2b2b;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
