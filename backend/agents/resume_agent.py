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
You are an expert ATS Resume Analyzer.

Analyze the following resume and extract structured information.

If a field cannot be determined, return an empty string or empty list.

Return ONLY valid JSON.

Do not explain anything.
Do not use markdown.
Do not wrap the JSON with ```.


Return this exact JSON structure.

- ats_score should be an integer between 0 and 100.
- strengths should contain 3-5 strengths.
- weaknesses should contain 3-5 weaknesses.

{{
    "name": "",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "ats_score": 85,
    "strengths": [
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "..."
    ]
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