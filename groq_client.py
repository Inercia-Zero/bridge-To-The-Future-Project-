
import base64
import os
import streamlit as st
from groq import Groq

TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

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
                    "content": "Você é um assistente acadêmico didático, humano e organizado. Responda em português do Brasil com clareza, boa estrutura e profundidade útil.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.28,
            max_tokens=1000,
        )
        text = (resp.choices[0].message.content or "").strip()
        return text if text else "Não consegui gerar uma resposta útil."
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

def ask_vision_ai(prompt: str, image_path: str) -> str:
    client, client_error = _load_client()
    if client is None:
        return client_error or "Não foi possível iniciar a IA."

    if not os.path.exists(image_path):
        return "Imagem não encontrada para análise."

    ext = os.path.splitext(image_path)[1].lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    try:
        resp = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente acadêmico didático. Analise a imagem com cuidado e responda em português do Brasil.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    ],
                },
            ],
            temperature=0.2,
            max_tokens=1200,
        )
        text = (resp.choices[0].message.content or "").strip()
        return text if text else "Não consegui gerar uma resposta útil."
    except Exception as e:
        return f"Erro ao analisar imagem: {e}"
