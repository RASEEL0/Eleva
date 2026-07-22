import json
import re

from config.llm import llm
from graph.state import CareerState
from agents.utils import safe_json_parse


def generate_interview_questions(
    target_job: str,
    resume_data: dict,
    missing_skills: list[str]
):

    prompt = f"""
You are an expert Technical Interviewer and Hiring Manager.

The candidate is applying for:
{target_job}

Candidate resume information:
{json.dumps(resume_data, indent=2)}

Missing skills:
{missing_skills}


Generate interview preparation material.

Requirements:
- Create technical questions related to the target job.
- Include questions about the candidate's projects and experience.
- Include questions about missing skills.
- Include behavioral questions based on the candidate background.
- Provide realistic expected answers or preparation tips.

Return ONLY valid JSON.

Do not explain anything.
Do not use markdown.
Do not wrap with ```.

Return this exact format:

{{
    "technical_questions": [
        {{
            "question": "",
            "expected_answer": ""
        }}
    ],

    "project_questions": [
        {{
            "question": "",
            "expected_answer": ""
        }}
    ],

    "behavioral_questions": [
        {{
            "question": "",
            "tips": ""
        }}
    ]
}}
"""

    response = llm.invoke(prompt)
    
    print("========== RAW RESPONSE ==========")
    print(response.content)
    print("==================================")

    content = response.content

    return safe_json_parse(content)



def interview_agent(state: CareerState):

    try:

        questions = generate_interview_questions(
            target_job=state["target_job"],
            resume_data=state.get(
                "resume_data",
                {}
            ),
            missing_skills=state.get(
                "missing_skills",
                []
            )
        )


        return {
            "interview_prep": questions,
            "status": "Interview preparation generated"
        }


    except Exception as e:

        return {
            "interview_prep": {},
            "status": f"Interview Prep Failed: {str(e)}"
        }