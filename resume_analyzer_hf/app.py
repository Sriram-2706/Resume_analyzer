from flask import Flask, request, jsonify
from utils.parser_local import extract_text
from utils.section_mapper import split_sections
from utils.ner_extractor import exp_project_entities
from utils.skills_matcher import match_skills
from utils.ats_check import ats_check
from utils.issue_detector import detect_issues, action_verb_penalty, impact_bonus
from utils.scorer import score_resume, grade_from_score
from utils.recommender import generate_recommendations
import os

app = Flask(__name__)

@app.get("/")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/analyze")
def analyze():
    if "file" not in request.files: return jsonify({"error":"no file"}), 400
    f = request.files["file"]; path = f"tmp_{f.filename}"; f.save(path)
    try:
        text = extract_text(path)
        sections = split_sections(text)
        ner_entities, dates = exp_project_entities(sections)
        matched_skills, missing_skills = match_skills(sections)
        ats = ats_check(f.filename, text)
        issues = detect_issues(sections, ner_entities, dates, matched_skills)
        pen, verb_count = action_verb_penalty(sections)
        bon, impact = impact_bonus(sections)

        profile_score = 100 if sections.get("profile_summary") else 50
        exp_score     = 100 if sections.get("experience") else 50
        skills_score  = 100 if sections.get("skills") else 50
        edu_score     = 100 if sections.get("education") else 50
        ats_score     = 100 if not ats["ats_issues"] else 50
        skills_bonus  = min(10, max(0, len(matched_skills) - 8))

        final_score = score_resume(profile_score, exp_score, skills_score, edu_score, ats_score, pen, bon, skills_bonus)
        grade = grade_from_score(final_score)
        recs = generate_recommendations(issues, ner_entities, matched_skills, missing_skills)

        return jsonify({
            "score": final_score,
            "grade": grade,
            "ats_issues": ats["ats_issues"],
            "issues": issues,
            "recommendations": recs,
            "entities": ner_entities,
            "dates": dates,
            "impact": impact,
            "action_verbs": verb_count,
            "skills_matched": matched_skills,
            "skills_missing": missing_skills[:20]
        }), 200
    finally:
        if os.path.exists(path): os.remove(path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
