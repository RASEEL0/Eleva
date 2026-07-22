import json
import re

from config.llm import llm
from graph.state import CareerState
from agents.utils import safe_json_parse


def generate_application_package(
    resume_data: dict,
    target_job: str,
    match_score: float
):
    prompt = f"""
You are an expert Career Advisor and HR specialist.

The candidate is applying for this role:
{target_job}

They achieved a match score of {match_score}%.

Here is the candidate's parsed resume:

{json.dumps(resume_data, indent=2)}

Create a personalized application package for this candidate.

Return ONLY valid JSON.

Do not explain anything.
Do not use markdown.
Do not wrap the response with ```.

Return this exact format:

{{
    "application_summary": "",
    "talking_points": [],
    "checklist": []
}}
"""

    response = llm.invoke(prompt)
    

    print("========== RAW RESPONSE ==========")
    print(response.content)
    print("==================================")
    
    content = response.content
    # Extract JSON from the LLM response
    return safe_json_parse(content)


def application_agent(state: CareerState):
    try:
        package = generate_application_package(
            state.get("resume_data", {}),
            state["target_job"],
            state.get("match_score", 0.0)
        )

        return {
    "application_package": package
}

    except Exception as e:
        return {
        "application_package": {},
        "status": f"Application Package Failed: {str(e)}"   # was "error"
    }