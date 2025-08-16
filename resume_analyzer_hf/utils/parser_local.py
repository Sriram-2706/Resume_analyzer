import os
import docx2txt
import pdfplumber
from pyresparser import ResumeParser

def extract_text_fallback(file_path: str) -> str:
    p = file_path.lower()
    if p.endswith(".docx"):
        return docx2txt.process(file_path) or ""
    elif p.endswith(".pdf"):
        out = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                out.append(page.extract_text() or "")
        return "\n".join(out)
    else:
        raise ValueError("Unsupported file format")

def read_bytes(file) -> str:
    tmp = f"tmp_{file.name}"
    with open(tmp, "wb") as f:
        f.write(file.getbuffer())
    try:
        text = ""
        try:
            data = ResumeParser(tmp).get_extracted_data()
            # Merge relevant fields to form full text
            fields = ["name", "email", "phone", "degree", "college", "skills", "company_names", "designation", "projects"]
            text = " ".join([str(data.get(f, "")) for f in fields if data.get(f)])
            # If PyResparser extracted nothing, fallback
            if not text.strip():
                text = extract_text_fallback(tmp)
        except Exception:
            # Any parser error, fallback
            text = extract_text_fallback(tmp)
        return text
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
