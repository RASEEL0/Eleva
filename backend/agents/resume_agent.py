from pypdf import PdfReader
from config.llm import llm
from graph.state import CareerState

import json
import re


def extract_resume_text(pdf_path: str) -> str:
    """
    Extract all text from the uploaded resume.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def analyze_resume(text: str) -> dict:

    prompt = f"""
You are an expert ATS Resume Analyzer and career coach.

Analyze the resume below and extract ALL technical and professional information.

Important rules:
- Extract every programming language, framework, tool, database, cloud technology, AI technology, and software tool mentioned in the resume.
- Do not summarize skills.
- Do not remove skills because they appear inside projects or experience.
- Include skills from the "Technical Skills", "Hard Skills", projects, education, and work experience sections.
- Keep the skill names exactly as they appear in the resume.
- Return ONLY valid JSON.

Return this exact structure:

{{
    "name": "",
    "skills": [
        "example: Python",
        "example: Java",
        "example: SQL"
    ],
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

    return json.loads(match.group())


def resume_agent(state: CareerState):

    try:
        text = extract_resume_text(state["resume_path"])

        resume_data = analyze_resume(text)

        return {
    "resume_text": text,
    "resume_data": resume_data,
    "ats_score": resume_data.get("ats_score", 0),
    "strengths": resume_data.get("strengths", []),
    "weaknesses": resume_data.get("weaknesses", [])
}

    except Exception as e:
        return {
        "resume_text": "",
        "resume_data": {},
        "ats_score": 0,
        "strengths": [],
        "weaknesses": [],
        "status": f"Resume Analysis Failed: {str(e)}"
    }