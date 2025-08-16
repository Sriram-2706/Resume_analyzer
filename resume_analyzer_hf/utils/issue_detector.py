import re
from typing import Tuple, Dict

ACTION_VERBS = [
    "developed","designed","led","implemented","created","managed","built","organized","initiated",
    "planned","executed","improved","optimized","coordinated","analyzed","delivered","launched",
    "reduced","increased","architected","owned","migrated"
]
BUZZWORDS = ["team player","dynamic professional","results-driven","self-starter","synergy","go-getter"]

def _count_action_verbs(text: str) -> int:
    tl = text.lower()
    return sum(len(re.findall(rf"\b{re.escape(v)}\b", tl)) for v in ACTION_VERBS)

def _impact_counts(text: str) -> Dict[str,int]:
    tl = (text or "").lower()
    return {
        "numbers": len(re.findall(r"\b\d{1,3}(?:[,\d]{0,6})\b", tl)),
        "percent": len(re.findall(r"\b\d{1,3}\s*%|\bpercent\b", tl)),
        "money": len(re.findall(r"[$₹€£]\s?\d", tl)),
        "scale_words": len(re.findall(r"\b(k|thousand|million|billion|crore|lakh)s?\b", tl))
    }

def action_verb_penalty(sections: dict) -> Tuple[int,int]:
    exp = sections.get("experience","") or ""
    pro = sections.get("projects","") or ""
    total = _count_action_verbs(exp) + _count_action_verbs(pro)
    thr = 3
    pen = (total - thr) * 5 if total > thr else 0
    return pen, total

def impact_bonus(sections: dict) -> Tuple[int,Dict[str,int]]:
    block = (sections.get("experience","") or "") + "\n" + (sections.get("projects","") or "")
    c = _impact_counts(block)
    bonus = min(10, 2 * sum(1 for v in c.values() if v > 0))
    return bonus, c

def detect_issues(sections: dict, ner_entities: dict, dates: list, matched_skills: list) -> dict:
    issues = {"profile_summary": {}, "education": {}, "work_experience": {}, "projects": {}, "skills": {}}
    ps = sections.get("profile_summary","") or ""
    edu = sections.get("education","") or ""
    exp = sections.get("experience","") or ""

    buzz = sum(1 for b in BUZZWORDS if b in ps.lower())
    if buzz: issues["profile_summary"]["buzzwords"] = buzz
    if not re.search(r"(B\.?E|B\.?Tech|B\.?Sc|M\.?Tech|MBA|Bachelor|Master|PhD|BCA|MCA)", edu, re.I):
        issues["education"]["missing_degree"] = 1
    if not re.search(r"\b(19|20)\d{2}\b", edu):
        issues["education"]["missing_year"] = 1

    years = sorted(map(int, re.findall(r"(19|20)\d{2}", exp)))
    gaps = sum(1 for i in range(1, len(years)) if years[i]-years[i-1] > 1)
    if gaps: issues["work_experience"]["career_gaps"] = gaps

    if not ner_entities.get("ORG"):
        issues["work_experience"]["no_org_entities"] = 1

    if len(matched_skills) < 5:
        issues["skills"]["low_coverage"] = len(matched_skills)

    return issues
