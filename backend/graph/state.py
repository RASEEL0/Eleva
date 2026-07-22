from typing import TypedDict


class CareerState(TypedDict):
    """
    Shared state that all agents can read and update.
    """

    user_id: str

    resume_path: str

    target_job: str

    resume_data: dict

    required_skills: list[str]

    missing_skills: list[str]

    match_score: float

    status: str

    learning_plan: dict

    optimized_resume: str

    interview_questions: list[str]

    next_action: str