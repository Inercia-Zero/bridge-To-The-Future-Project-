import os
import random
import streamlit as st
from groq import Groq

from prompts import build_prompt, is_smalltalk
from mentors import MENTORS
from database import (
    init_db,
    listar_conversas,
    criar_conversa,
    salvar_mensagem,
    carregar_mensagens,
    deletar_conversa,
    renomear_conversa,
)

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Bridge to the Future",
    page_icon="🎓",
    layout="wide"
)

# =========================
# INIT
# =========================
init_db()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# SESSION STATE
# =========================
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None

if "profile" not in st.session_state:
    st.session_state.profile = "Aluno"

if "selected_area" not in st.session_state:
    st.session_state.selected_area = list(MENTORS.keys())[0]


# =========================
# HELPERS
# =========================
def gerar_resposta_curta():
    respostas = [
        "E aí! Bora estudar o quê?",
        "Fala! O que você quer aprender hoje?",
        "Manda a dúvida 😄",
        "Bora! Qual é o desafio?",
        "Pode perguntar sem medo 👊",
        "Aqui não tem erro... só cálculo 😂",
    ]
    return random.choice(respostas)


def garantir_conversa_ativa():
    if st.session_state.current_conversation is None:
        conversas = listar_conversas()
        if conversas:
            st.session_state.current_conversation = conversas[0]["id"]


def gerar_titulo_inicial(user_input: str) -> str:
    texto = (user_input or "").strip()
    if not texto:
        return "Nova conversa"
    return texto[:40]


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    if os.path.exists("logoifce.png"):
        st.image("logoifce.png", use_container_width=True)
    elif os.path.exists("logoprojeto.png"):
        st.image("logoprojeto.png", use_container_width=True)

    st.markdown("## Bridge to the Future")

    st.radio(
        "Perfil",
        ["Aluno", "Professor"],
        key="profile"
    )

    st.selectbox(
        "Área",
        list(MENTORS.keys()),
        key="selected_area"
    )

    if st.button("➕ Nova conversa", use_container_width=True):
        nova_id = criar_conversa("Nova conversa")
        st.session_state.current_conversation = nova_id
        st.rerun()

    st.markdown("### Histórico")

    conversas = listar_conversas()

    if not conversas:
        st.caption("Nenhuma conversa ainda.")
    else:
        for conv in conversas:
            col1, col2 = st.columns([4, 1])

            with col1:
                if st.button(conv["title"], key=f"open_{conv['id']}", use_container_width=True):
                    st.session_state.current_conversation = conv["id"]
                    st.rerun()

            with col2:
                if st.button("⋮", key=f"menu_{conv['id']}", use_container_width=True):
                    st.session_state[f"menu_{conv['id']}"] = not st.session_state.get(f"menu_{conv['id']}", False)

            if st.session_state.get(f"menu_{conv['id']}", False):
                novo_nome = st.text_input("Renomear conversa", key=f"rename_input_{conv['id']}")

                if st.button("Salvar nome", key=f"save_name_{conv['id']}", use_container_width=True):
                    if novo_nome.strip():
                        renomear_conversa(conv["id"], novo_nome.strip())
                        st.rerun()

                if st.button("🗑️ Apagar conversa", key=f"delete_{conv['id']}", use_container_width=True):
                    deletar_conversa(conv["id"])

                    if st.session_state.current_conversation == conv["id"]:
                        st.session_state.current_conversation = None

                    st.rerun()

# =========================
# MAIN
# =========================
garantir_conversa_ativa()

st.title("Bridge to the Future")

area = st.session_state.selected_area
mentor_data = MENTORS[area]

st.caption(f"Área ativa: {area}")

if st.session_state.current_conversation is None:
    st.info("Crie ou abra uma conversa para começar.")
    st.stop()

mensagens = carregar_mensagens(st.session_state.current_conversation)

for msg in mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input(f"Converse com a área de {area.lower()}...")

if user_input:
    # se a conversa ainda estiver com título padrão e for a primeira mensagem, renomeia
    conversas = listar_conversas()
    conversa_atual = next((c for c in conversas if c["id"] == st.session_state.current_conversation), None)

    if conversa_atual and conversa_atual["title"] == "Nova conversa" and len(mensagens) == 0:
        renomear_conversa(
            st.session_state.current_conversation,
            gerar_titulo_inicial(user_input)
        )

    salvar_mensagem(st.session_state.current_conversation, "user", user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    if is_smalltalk(user_input):
        resposta = gerar_resposta_curta()
    else:
        try:
            prompt = build_prompt(
                user_input=user_input,
                mentor=area,
                profile=st.session_state.profile,
                history=mensagens,
                context_text=None,
                context_file_name=None,
                context_file_type=None,
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

            resposta = response.choices[0].message.content

            if not resposta:
                resposta = "Tive um problema ao responder agora. Pode repetir?"

        except Exception as e:
            resposta = f"Erro ao gerar resposta: {e}"

    salvar_mensagem(st.session_state.current_conversation, "assistant", resposta)

    with st.chat_message("assistant"):
        st.markdown(resposta)

    st.rerun()
