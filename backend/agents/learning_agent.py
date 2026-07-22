import json
import re

from config.llm import llm
from graph.state import CareerState


def generate_learning_plan(missing_skills: list[str], target_job: str):

    prompt = f"""
You are an AI career learning coach.

A user wants to become a {target_job}.

They are missing these skills:

{missing_skills}

Create a realistic learning roadmap.

Return ONLY valid JSON.

Do not explain anything.
Do not use markdown.
Do not wrap with ```.

Return this format:

{{
    "goal": "",
    "estimated_duration": "",
    "learning_steps": [
        {{
            "skill": "",
            "why_needed": "",
            "tasks": [],
            "estimated_time": ""
        }}
    ],
    "projects_to_build": []
}}
"""

    response = llm.invoke(prompt)

    content = response.content

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in LLM response")

    return json.loads(match.group())


def learning_agent(state: CareerState):

    try:

        plan = generate_learning_plan(
            state["missing_skills"],
            state["target_job"]
        )

        return {
            "learning_plan": plan
        }


    except Exception as e:

        return {
            "learning_plan": {},
            "status": f"Learning Plan Failed: {str(e)}"
        }