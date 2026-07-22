import json
import re

from config.llm import llm
from graph.state import CareerState
from agents.utils import safe_json_parse


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

    return safe_json_parse(content)


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