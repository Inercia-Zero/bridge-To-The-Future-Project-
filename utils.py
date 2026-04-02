from datetime import datetime
import re

def now_iso() -> str:
    return datetime.utcnow().isoformat()

def clean_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", (text or "").strip())

def get_first_name(name: str) -> str:
    name = (name or "").strip()
    return name.split()[0] if name else "Usuário"
