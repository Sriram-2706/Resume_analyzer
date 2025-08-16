import re
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer, util
from utils.skill_extractor import extract_skills

_SKILL_BANK = [
    "python","java","c++","javascript","typescript","react","node.js","django","flask",
    "sql","mysql","postgresql","mongodb","redis","aws","azure","gcp","docker","kubernetes",
    "terraform","linux","git","ci/cd","jenkins","spark","hadoop","pandas","numpy",
    "scikit-learn","pytorch","tensorflow","nlp","computer vision","rest api","graphql",
    "microservices","agile","jira","tableau","power bi"
]

_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
_BANK_EMB = _model.encode(_SKILL_BANK, convert_to_tensor=True)

def _candidates_from_text(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z\+\#\./-]{1,25}", text or "")
    phrases = re.findall(r"[A-Za-z][A-Za-z0-9\+\#\./ -]{2,}", text or "")
    cleaned = [t.lower() for t in tokens+phrases if len(t) > 2 and len(t)<=30 and not t.startswith("##")]
    return sorted(set(cleaned))

def match_skills(sections: Dict[str,str], topk: int = 50, thresh: float = 0.55) -> Tuple[List[str], List[str], List[str]]:
    block = " ".join([sections.get("skills",""), sections.get("experience",""), sections.get("projects","")])
    if not block: return [], _SKILL_BANK, []

    ner_cands = extract_skills(block)
    regex_cands = _candidates_from_text(block)
    cands = list(set(ner_cands + regex_cands))
    if not cands: return [], _SKILL_BANK, []

    C = _model.encode(cands, convert_to_tensor=True)
    sim = util.cos_sim(C, _BANK_EMB)

    hits = set()
    for i, row in enumerate(sim):
        j = int(row.argmax())
        if float(row[j]) >= thresh:
            hits.add(_SKILL_BANK[j])

    matched = sorted(hits)
    missing = [s for s in _SKILL_BANK if s not in matched]
    extras = [c for c in ner_cands if c not in _SKILL_BANK and len(c) > 2 and not c.startswith("##")]

    return matched[:topk], missing, extras
