Offline AI-Powered Resume Analyzer - Trojan Hex
=================================

Description
-----------
This tool analyzes resumes locally using Hugging Face pipelines and custom logic. 
It extracts key sections, detects issues, scores resumes, and provides actionable recommendations — similar to platforms like Resume Worded or JobScan.

Quick Version: An offline resume analyzer that works like Resume Worded/JobScan — extracts sections, checks ATS issues, scores resumes, and gives improvement tips.

Features
--------
- Extracts Profile Summary, Experience, Education, Skills, Projects, Achievements
- Detects action verbs, career gaps, missing skills, buzzwords, ATS issues
- Scores resumes and assigns a grade (A–D)
- Generates personalized improvement recommendations
- Works with PDF and DOCX files, including two-column formats
- No internet required; uses offline Hugging Face models

Installation
------------
1. Clone the repository:
   git clone <repo_url>
   cd <repo_folder>

2. Install dependencies:
   pip install -r requirements.txt

3. Install Pyresparser system dependencies (for resume parsing):  
   - Linux/macOS: sudo apt-get install python3-tk python3-dev build-essential  
   - Windows: Ensure Microsoft Visual C++ Build Tools is installed

Usage
-----
Run the Streamlit app:
   streamlit run streamlit_app.py

Upload a resume in PDF or DOCX format. The app will display:
- Section-wise extracted content
- NER entities and achievements
- Matched skills, missing skills, extra skills
- Resume score and grade
- Detailed issue analysis and improvement recommendations

Project Structure
-----------------
utils/
├─ parser_local.py       # Handles PDF/DOCX reading
├─ section_mapper.py     # Splits text into sections
├─ ner_extractor.py      # Extracts entities and achievements
├─ skill_extractor.py    # NER-based skill detection
├─ skills_matcher.py     # Matches skills to skill bank
├─ issue_detector.py     # Detects issues and penalties
├─ scorer.py             # Computes score and grade
├─ recommender.py        # Generates improvement recommendations
├─ ats_check.py          # Checks ATS compatibility
streamlit_app.py         # Streamlit UI entrypoint
requirements.txt         # Python dependencies

Notes
-----
- For best results, use clean PDF/DOCX resumes. Two-column formats are supported.
- Achievements are extracted only from sections explicitly marked as Achievements.
- Profile summary is auto-generated if missing.

License
-------
MIT License
