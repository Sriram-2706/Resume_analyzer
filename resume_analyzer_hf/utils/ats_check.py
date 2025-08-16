def ats_check(file_path: str, text: str) -> dict:
    issues = []
    if not file_path.lower().endswith((".pdf",".docx")):
        issues.append("Unsupported file format")
    if len(text) > 20000:
        issues.append("Resume too long (>20k chars)")
    return {"ats_issues": issues}
