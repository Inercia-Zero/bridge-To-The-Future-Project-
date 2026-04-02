import streamlit as st
from groq import Groq

TEXT_MODEL = "llama-3.3-70b-versatile"

def _load_client():
    try:
        key = str(st.secrets.get("GROQ_API_KEY", "")).strip()
    except Exception:
        key = ""

    if not key:
        return None, "A chave GROQ_API_KEY não foi encontrada nos Secrets."

    try:
        return Groq(api_key=key), None
    except Exception as e:
        return None, f"Erro ao iniciar Groq: {e}"

def ask_ai(prompt: str) -> str:
    client, client_error = _load_client()
    if client is None:
        return client_error or "Não foi possível iniciar a IA."

    try:
        resp = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente acadêmico didático. "
                        "Responda em português do Brasil com clareza, organização e didática."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.25,
            max_tokens=900,
        )
        text = (resp.choices[0].message.content or "").strip()
        return text if text else "Não consegui gerar uma resposta útil."
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"
