import streamlit as st

from theme import apply_theme
from mentors import MENTORS
from database import init_db
from prompts import build_prompt
from groq_client import ask_ai

# Configuração
st.set_page_config(page_title="Bridge to the Future", layout="wide")

# Tema
apply_theme()

# Banco
init_db()

# Interface
st.title("Bridge to the Future 🚀")
st.caption("Projeto educacional para estudantes da rede pública.")

mentor = st.selectbox(
    "Escolha o mentor:",
    list(MENTORS.keys())
)

mentor_info = MENTORS[mentor]
st.markdown(f"**{mentor_info['title']}**")
st.caption(mentor_info["description"])

user_input = st.text_input("Digite sua dúvida:")

if user_input:
    try:
        prompt = build_prompt(user_input, mentor)
        resposta = ask_ai(prompt)
        st.write(resposta)
    except Exception as e:
        st.error(f"Erro ao gerar resposta: {e}")
