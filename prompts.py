import re
import unicodedata
from mentors import MENTORS


def normalize_text(text: str) -> str:
    text = (text or "").strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)
    return text


def is_smalltalk(user_input: str) -> bool:
    t = normalize_text(user_input)
    t = t.rstrip("?!.,;:")

    gatilhos_exatos = {
        "oi", "olá", "ola", "oie",
        "opa", "eae", "e ai",
        "fala", "fala cmg", "fala comigo",
        "bom dia", "boa tarde", "boa noite",
        "tudo bem", "suave", "blz", "beleza"
    }

    if t in gatilhos_exatos:
        return True

    if len(t) <= 15 and any(g in t for g in gatilhos_exatos):
        return True

    return False

def build_prompt(
    user_input: str,
    mentor: str,
    profile: str = "Aluno",
    history: list | None = None,
    context_text: str | None = None,
    context_file_name: str | None = None,
    context_file_type: str | None = None,
) -> str:
    mentor_data = MENTORS.get(mentor, {})
    system_prompt = mentor_data.get("system_prompt", "")

    history_text = ""
    if history:
        lines = []
        for item in history[-4:]:
            who = "Usuário" if item["role"] == "user" else "Assistente"
            lines.append(f"{who}: {item['content']}")
        history_text = "\n".join(lines)

    profile_block = (
        "Você está falando com um PROFESSOR. Use linguagem técnica, organizada e objetiva."
        if profile == "Professor"
        else "Você está falando com um ALUNO. Use linguagem acolhedora, didática e passo a passo."
    )

    context_block = ""
    if context_text:
        context_block = (
            f"Há um arquivo anexado nesta conversa.\n"
            f"Nome: {context_file_name}\n"
            f"Tipo: {context_file_type}\n"
            f"Conteúdo extraído:\n{context_text[:4000]}"
        )
    elif context_file_type == "image":
        context_block = (
            f"Há uma imagem anexada nesta conversa.\n"
            f"Nome: {context_file_name}\n"
            f"Tipo: {context_file_type}\n"
            f"Analise visualmente essa imagem junto com o pedido do usuário."
        )

    scope_block = (
        f"Você está dentro do mestre de {mentor}. "
        f"Se o pedido do usuário pertencer claramente a outra área, avise com educação que ele deve voltar à tela inicial e escolher outro mestre."
    )

    style_block = (
        "Quando o input for simples e social, responda de forma curta, natural e humana. "
        "Quando a dúvida for acadêmica, organize bem a resposta. "
        "Você pode usar humor leve e contextual ligado ao conteúdo estudado, mas sem exagerar."
    )

    return f"""{system_prompt}

{profile_block}

{scope_block}

Área selecionada: {mentor}

Histórico recente:
{history_text if history_text else "Sem histórico anterior."}

Contexto adicional:
{context_block if context_block else "Sem arquivo adicional nesta conversa."}

Pergunta do usuário:
{user_input}

Regras de resposta:
- Responda em português do Brasil.
- Organize a resposta com boa estrutura visual.
- Se houver matemática ou física, use LaTeX válido.
- Use $...$ para expressões curtas e $$...$$ para fórmulas destacadas.
- Explique o significado antes de aplicar fórmulas importantes.
- Quando houver caminho simples e caminho completo, separe claramente os dois.
- Quando houver propriedade matemática ou física, diga por que ela vale naquele passo.
- Não faça respostas gigantes para saudações simples.
- Seja humano, direto e didático.

Estilo:
{style_block}
"""
