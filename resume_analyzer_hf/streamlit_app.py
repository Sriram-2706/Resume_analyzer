import streamlit as st
from utils.parser_local import read_bytes
from utils.section_mapper import split_sections
from utils.ner_extractor import exp_project_entities
from utils.skills_matcher import match_skills
from utils.ats_check import ats_check
from utils.issue_detector import detect_issues, action_verb_penalty, impact_bonus
from utils.scorer import score_resume, grade_from_score
from utils.recommender import generate_recommendations

st.set_page_config(page_title="Resume Analyzer (Offline HF)", layout="wide")
st.title("📄 Offline Resume Analyzer — Hugging Face Pipelines")

file = st.file_uploader("Upload .pdf or .docx", type=["pdf","docx"])
if file:
    text = read_bytes(file)
    sections, profile_generated = split_sections(text)
    ner_entities, dates = exp_project_entities(sections)
    matched_skills, missing_skills, extra_skills = match_skills(sections)
    ats = ats_check(file.name, text)
    issues = detect_issues(sections, ner_entities, dates, matched_skills)
    pen, verb_count = action_verb_penalty(sections)
    bon, impact = impact_bonus(sections)

    profile_score = 100 if sections.get("profile_summary") else 50
    exp_score     = 100 if sections.get("experience") else 50
    skills_score  = 100 if matched_skills else 50
    edu_score     = 100 if sections.get("education") else 50
    ats_score     = 100 if not ats["ats_issues"] else 50

    skills_bonus = min(10, max(0, len(matched_skills) - 8))
    final_score = score_resume(profile_score, exp_score, skills_score, edu_score, ats_score, pen, bon, skills_bonus)
    grade = grade_from_score(final_score)
    recs = generate_recommendations(issues, missing_skills=missing_skills, extras=extra_skills)

    if profile_generated:
        st.warning("Profile summary was missing; generated automatically from education + experience (cleaned).")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Score", f"{final_score}/100")
    c2.metric("Grade", grade)
    c3.metric("Verb Hits", verb_count)
    c4.metric("Skill Matches", len(matched_skills))

    st.divider()
    st.subheader("Sections")
    for sec in ["profile_summary","experience","projects","education","skills","achievements"]:
        with st.expander(sec.replace("_"," ").title()):
            st.write(sections.get(sec) or "_none_")

    st.divider()
    st.subheader("NER Entities (Experience + Projects + Achievements)")
    st.json(ner_entities)

    st.subheader("Impact Signals")
    st.write(impact)
    st.write(f"Bonus: +{bon}")

    st.subheader("ATS Warnings")
    st.write(ats["ats_issues"] or "None")

    st.subheader("Matched Skills")
    st.write(matched_skills or "None")

    st.subheader("Suggested Skills to Add")
    st.write(missing_skills[:20] or "None")

    st.subheader("Extra Skills (Detected but not in Skill Bank)")
    st.write(extra_skills or "None")

    st.subheader("Recommendations")
    for r in recs: st.write(f"- {r}")
