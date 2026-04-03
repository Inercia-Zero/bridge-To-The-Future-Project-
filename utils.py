from datetime import datetime
import re

def now_iso() -> str:
    return datetime.utcnow().isoformat()

def clean_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", (text or "").strip())

def get_first_name(name: str) -> str:
    name = (name or "").strip()
    return name.split()[0] if name else "Usuário"

def infer_file_type(filename: str) -> str:
    name = (filename or "").lower()
    if name.endswith(".pdf"):
        return "pdf"
    if name.endswith(".txt"):
        return "text"
    if name.endswith((".png", ".jpg", ".jpeg", ".webp")):
        return "image"
    return "unknown"
