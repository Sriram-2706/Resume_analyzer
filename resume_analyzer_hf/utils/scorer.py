from typing import Dict
from utils.skills_matcher import match_skills

def score_resume(profile_ok, exp_ok, skills_ok, edu_ok, ats_ok, exp_penalty, exp_bonus, skills_bonus=0):
    base = (0.15*profile_ok + 0.35*exp_ok + 0.2*skills_ok + 0.15*edu_ok + 0.15*ats_ok)
    adjusted = max(0, min(100, base - exp_penalty + exp_bonus + skills_bonus))
    return round(adjusted, 2)

def grade_from_score(score: float) -> str:
    if score >= 85: return "A"
    elif score >= 70: return "B"
    elif score >= 55: return "C"
    else: return "D"

def compute_skill_scores(sections: Dict[str,str]):
    matched, missing, extras = match_skills(sections)
    skill_score = 100 if matched else 50
    return skill_score, matched, missing, extras
