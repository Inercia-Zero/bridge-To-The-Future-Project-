from mentors import MENTORS


def build_prompt(user_input: str, mentor: str) -> str:
    mentor_data = MENTORS.get(mentor, {})
    system_prompt = mentor_data.get("system_prompt", "")

    return f"""{system_prompt}

Área selecionada: {mentor}

Pergunta do usuário:
{user_input}

Responda em português do Brasil, de forma clara, organizada e didática.
Se houver fórmula, explique o significado antes de aplicar.
"""
