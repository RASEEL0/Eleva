import json
import re

from config.llm import llm
from graph.state import CareerState
from agents.utils import safe_json_parse


def analyze_job_requirements(job_title: str) -> dict:

    prompt = f"""
You are an expert technical recruiter and hiring manager.

Your task is to create a realistic job requirement profile.

The candidate is applying for this role:

Job Title:
{job_title}

Generate the common skills required for this position.

Return ONLY valid JSON.

Do not explain anything.
Do not use markdown.
Do not wrap the response with ```.

The JSON must contain:

{{
    "required_skills": [
        "skill1",
        "skill2",
        "skill3"
    ],
    "preferred_skills": [
        "skill1",
        "skill2"
    ],
    "responsibilities": [
        "responsibility1",
        "responsibility2"
    ]
}}

Important:
- required_skills must contain at least 8 technical skills.
- preferred_skills must contain at least 3 additional skills.
- responsibilities must contain at least 3 common responsibilities.

Generate the profile now.
"""

    response = llm.invoke(prompt)

    # print("========== RAW RESPONSE ==========")
    # print(response.content)
    # print("==================================")


    content = response.content

    return safe_json_parse(content)


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