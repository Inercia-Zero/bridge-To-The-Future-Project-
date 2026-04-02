import os
import uuid
from typing import Optional, Tuple
from pypdf import PdfReader

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_PDF_MB = 15
MAX_FILE_MB = 12

def file_mb(uploaded_file) -> float:
    return round(len(uploaded_file.getbuffer()) / (1024 * 1024), 2)

def validate_upload(uploaded_file) -> Optional[str]:
    name = uploaded_file.name.lower()
    mb = file_mb(uploaded_file)

    if name.endswith(".pdf"):
        if mb > MAX_PDF_MB:
            return f"O PDF excede o limite de {MAX_PDF_MB} MB."
        return None

    allowed = (".png", ".jpg", ".jpeg", ".webp", ".txt")
    if not name.endswith(allowed):
        return "Envie PDF, imagem (PNG/JPG/WEBP) ou TXT."

    if mb > MAX_FILE_MB:
        return f"O arquivo excede o limite de {MAX_FILE_MB} MB."
    return None

def save_upload(uploaded_file) -> Tuple[str, str, str]:
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    dest = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if ext == ".pdf":
        ftype = "pdf"
    elif ext == ".txt":
        ftype = "text"
    else:
        ftype = "image"

    return dest, uploaded_file.name, ftype

def extract_pdf_text(path: str) -> Optional[str]:
    try:
        reader = PdfReader(path)
        chunks = []
        for page in reader.pages:
            txt = (page.extract_text() or "").strip()
            if txt:
                chunks.append(txt)
        result = "\n\n".join(chunks).strip()
        return result or None
    except Exception:
        return None
