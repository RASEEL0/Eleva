from typing import TypedDict


class CareerState(TypedDict):
    # User
    user_id: str

    # Input
    resume_path: str
    target_job: str

    # Resume
    resume_text: str          
    resume_data: dict

    ats_score: float
    strengths: list[str]
    weaknesses: list[str]

    # Job
    required_skills: list[str]

    # Analysis
    missing_skills: list[str]
    match_score: float
    status: str

    # Outputs
    learning_plan: dict
    optimized_resume: str
    interview_questions: list[str]

    # Routing
    next_action: str