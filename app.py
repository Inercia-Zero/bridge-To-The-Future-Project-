import streamlit as st

from theme import apply.theme
from mentors import MENTORS
from database import init_db
from prompts import build_prompt
from groq_client import ask_ai

#Configuração
st.set_page_confi(page_tilte="Brigde to the future", layout="wide")

#Tema
apply_theme()

#Banco
init_db()

#interface
st.title("bridge to the future 🚀")

user_imput = st.text_input("digite sua dúvida:")

if user_input:
  prompt = build_prompt(user_input, mentor)
  resposta = ask_ai(prompt)
  
