import json
import re

from config.llm import llm
from graph.state import CareerState


def analyze_job_requirements(job_title: str) -> dict:

    prompt = f"""
You are an experienced technical recruiter.

Given the following job title:

{job_title}

Return ONLY valid JSON.

Do not explain anything.
Do not use markdown.
Do not wrap the JSON with ```.

Return this format exactly:

{{
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": []
}}
"""

    response = llm.invoke(prompt)

    content = response.content

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in LLM response.")

    return json.loads(match.group())


def job_agent(state: CareerState):

    try:
        job_data = analyze_job_requirements(state["target_job"])

        return {
            "required_skills": job_data.get("required_skills", [])
        }

    except Exception as e:
        return {
            "required_skills": [],
            "status": f"Job Analysis Failed: {str(e)}"
        }