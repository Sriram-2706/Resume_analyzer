import re
from transformers import pipeline

_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
LABELS = ["profile_summary", "experience", "education", "skills", "projects", "achievements"]

def _paragraphs(text: str):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    merged, buf = [], []
    for line in lines:
        line = re.sub(r"\s{2,}|\t", " ", line)  # handle two-column layouts
        buf.append(line)
        if len(" ".join(buf)) > 300:
            merged.append(" ".join(buf))
            buf = []
    if buf:
        merged.append(" ".join(buf))
    return merged

def _extract_education(text: str):
    edu_lines = []
    for line in text.split("\n"):
        if re.search(r"education|bachelor|master|college|institute|cgpa|degree", line, re.I):
            edu_lines.append(line)
    return "\n".join(edu_lines)

def split_sections(text: str) -> tuple[dict,bool]:
    sections = {k: "" for k in LABELS}
    profile_generated = False

    for para in _paragraphs(text):
        r = _classifier(para, candidate_labels=LABELS, multi_label=False)
        best = r["labels"][0]
        sections[best] = (sections[best] + ("\n" if sections[best] else "") + para).strip()

    if sections["education"]:
        sections["education"] = _extract_education(sections["education"])

    if not sections["profile_summary"]:
        summary_lines = []
        if sections["education"]:
            summary_lines.append(sections["education"].split("\n")[0])
        if sections["experience"]:
            first_exp_line = sections["experience"].split("\n")[0]
            first_exp_line = re.sub(r"[^\w\s.,]", "", first_exp_line)
            summary_lines.append(first_exp_line)
        sections["profile_summary"] = " ".join(summary_lines)
        profile_generated = True

    return sections, profile_generated
