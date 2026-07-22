import json
import re

from config.llm import llm
from graph.state import CareerState
from agents.utils import safe_json_parse


def generate_resume_improvements(
    resume_data: dict,
    target_job: str,
    missing_skills: list[str],
    match_score: float
):

    prompt = f"""
You are an expert Resume Writer and ATS Optimization Specialist.

The candidate is applying for:
{target_job}

Current ATS match score:
{match_score}%

Missing skills:
{missing_skills}

Current resume information:

{json.dumps(
    resume_data,
    indent=2,
    ensure_ascii=False
)}

Analyze the resume and suggest improvements to increase the chance of passing ATS systems.

Focus on:
- Adding missing keywords naturally
- Improving project descriptions
- Improving professional summary
- Strengthening backend/software engineering experience
- Making bullet points achievement-oriented

Return ONLY valid JSON.

Do not explain anything.
Do not use markdown.
Do not wrap with ```.

Return this exact format:

{{
    "summary_suggestion": "",

    "bullet_point_improvements": [
        {{
            "section": "",
            "original": "",
            "improved": ""
        }}
    ],

    "keywords_to_add": [],

    "general_recommendations": []
}}
"""


    response = llm.invoke(prompt)

    content = response.content


    return safe_json_parse(content)



def resume_improvement_agent(state: CareerState):

    try:

        improvements = generate_resume_improvements(
            state.get("resume_data", {}),
            state["target_job"],
            state.get("missing_skills", []),
            state.get("match_score", 0)
        )


        return {
    "resume_improvements": improvements,
    "status": "Resume improvement generated successfully."
}


    except Exception as e:

        return {
            "resume_improvements": {},
            "status": f"Resume Improvement Failed: {str(e)}"
        }