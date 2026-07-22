from pypdf import PdfReader
from config.llm import llm
from graph.state import CareerState

import json
import re


def extract_resume_text(pdf_path: str) -> str:
    """
    Extract all text from a PDF resume.
    """

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def analyze_resume(text: str) -> dict:
    """
    Analyze the resume using the LLM and return structured JSON.
    """

    prompt = f"""
You are an expert ATS Resume Analyzer and Career Coach.

Your job is to read the resume and extract ALL information.

IMPORTANT RULES

1. Extract the candidate's full name.
2. Extract EVERY technical skill that appears anywhere in the resume.
3. Do NOT summarize skills.
4. Include skills from:
   - Skills section
   - Technical Skills
   - Hard Skills
   - Projects
   - Experience
   - Education
   - Certifications
5. Preserve the original skill names.
6. Never invent information.
7. Return ONLY valid JSON.
8. Do NOT wrap the response in markdown.

ATS SCORE
- Return an integer between 0 and 100.

STRENGTHS
- Exactly 3 strengths.

WEAKNESSES
- Exactly 3 weaknesses.

Return exactly this JSON:

{{
    "name": "",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "ats_score": 0,
    "strengths": [],
    "weaknesses": []
}}

Resume:

{text}
"""

    response = llm.invoke(prompt)

    content = response.content

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in LLM response.")

    resume_data = json.loads(match.group())

    # -----------------------------
    # Safety defaults
    # -----------------------------

    resume_data.setdefault("name", "")
    resume_data.setdefault("skills", [])
    resume_data.setdefault("education", [])
    resume_data.setdefault("experience", [])
    resume_data.setdefault("projects", [])
    resume_data.setdefault("ats_score", 0)
    resume_data.setdefault("strengths", [])
    resume_data.setdefault("weaknesses", [])

    return resume_data


def resume_agent(state: CareerState):
    """
    Resume Agent
    1. Read PDF
    2. Extract text
    3. Analyze with LLM
    4. Save results into graph state
    """

    try:
        resume_text = extract_resume_text(state["resume_path"])

        resume_data = analyze_resume(resume_text)

        return {
            "resume_text": resume_text,
            "resume_data": resume_data,
            "ats_score": resume_data["ats_score"],
            "strengths": resume_data["strengths"],
            "weaknesses": resume_data["weaknesses"],
        }

    except Exception as e:

        return {
            "resume_text": "",
            "resume_data": {},
            "ats_score": 0,
            "strengths": [],
            "weaknesses": [],
            "status": f"Resume Analysis Failed: {e}"
        }