import re
from transformers import pipeline

_ner = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple")

ACHIEVE_PATTERNS = [
    r"achieve", r"winner", r"rank", r"score", r"certification", r"qualified",
    r"air-\d+", r"top \d+%", r"finals"
]

def extract_entities(text: str):
    ents = _ner(text) if text else []
    out = {"PER": [], "ORG": [], "LOC": [], "MISC": [], "ACHIEVEMENTS":[]}
    for e in ents:
        lbl = e.get("entity_group", "")
        if lbl in out:
            val = e["word"].strip()
            if val not in out[lbl]: out[lbl].append(val)

    # extract achievements only if under Achievements section
    for line in text.split("\n"):
        for pat in ACHIEVE_PATTERNS:
            if re.search(pat, line, re.I):
                out["ACHIEVEMENTS"].append(line.strip())

    dates = re.findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b|\b(19|20)\d{2}\b", text, flags=re.I)
    out["ACHIEVEMENTS"] = sorted(set(out["ACHIEVEMENTS"]))
    return out, dates

def exp_project_entities(sections: dict):
    exp = sections.get("experience","") or ""
    pro = sections.get("projects","") or ""
    ach = sections.get("achievements","") or ""
    e_ents, e_dates = extract_entities(exp)
    p_ents, p_dates = extract_entities(pro)
    a_ents, a_dates = extract_entities(ach)
    merged = {k: sorted(set(e_ents.get(k, []) + p_ents.get(k, []) + a_ents.get(k, []))) for k in ["PER","ORG","LOC","MISC","ACHIEVEMENTS"]}
    dates = sorted(set([d if isinstance(d,str) else "".join(d) for d in e_dates+p_dates+a_dates]))
    return merged, dates
