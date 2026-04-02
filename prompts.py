from mentors import MENTORS

def build_prompt(user_input: str, mentor: str, history: list | None = None) -> str:
    mentor_data = MENTORS.get(mentor, {})
    system_prompt = mentor_data.get("system_prompt", "")

    history_text = ""
    if history:
        lines = []
        for item in history[-4:]:
            who = "Usuário" if item["role"] == "user" else "Assistente"
            lines.append(f"{who}: {item['content']}")
        history_text = "\n".join(lines)

    return f"""{system_prompt}

Área selecionada: {mentor}

Histórico recente:
{history_text if history_text else "Sem histórico anterior."}

Pergunta do usuário:
{user_input}

Responda em português do Brasil, de forma clara, organizada e didática.
Se houver fórmula, explique o significado antes de aplicar.
"""
