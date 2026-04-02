import streamlit as st

from theme import apply_theme
from mentors import MENTORS
from database import init_db
from prompts import build_prompt
from groq_client import ask_ai

st.set_page_config(
    page_title="Bridge to the Future",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_db()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mentor" not in st.session_state:
    st.session_state.mentor = "Matemática"

with st.sidebar:
    st.title("Bridge to the Future")
    st.caption("Projeto educacional para estudantes da rede pública.")
    st.session_state.mentor = st.selectbox(
        "Escolha o mentor",
        list(MENTORS.keys()),
        index=list(MENTORS.keys()).index(st.session_state.mentor),
    )

mentor_info = MENTORS[st.session_state.mentor]

st.title("Bridge to the Future 🚀")
st.caption("Projeto educacional para estudantes da rede pública.")
st.subheader(mentor_info["title"])
st.write(mentor_info["description"])

for item in st.session_state.chat_history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

user_input = st.chat_input("Digite sua dúvida...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            prompt = build_prompt(
                user_input=user_input,
                mentor=st.session_state.mentor,
                history=st.session_state.chat_history[:-1],
            )
            resposta = ask_ai(prompt)
        except Exception as e:
            resposta = f"Erro ao gerar resposta: {e}"

        st.markdown(resposta)
        st.session_state.chat_history.append({"role": "assistant", "content": resposta})
