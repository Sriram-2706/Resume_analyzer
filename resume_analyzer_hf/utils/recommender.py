def generate_recommendations(issues, missing_skills=None, extras=None):
    recs = []
    for sec, msg in issues.items():
        if msg:
            recs.append(f"Improve {sec}: {msg}")
        else:
            recs.append(f"Good job on {sec}!")
    if missing_skills:
        recs.append("Consider adding these missing key skills: " + ", ".join(missing_skills[:10]))
    if extras:
        recs.append("Highlight your extra skills beyond ATS keywords: " + ", ".join(extras[:5]))
    return recs
