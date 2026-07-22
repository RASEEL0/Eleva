from typing import TypedDict


class CareerState(TypedDict):

    # ==========================
    # User Input
    # ==========================
    user_id: str
    resume_path: str
    target_job: str


    # ==========================
    # Resume Analysis
    # ==========================
    resume_text: str
    resume_data: dict

    ats_score: float
    strengths: list[str]
    weaknesses: list[str]


    # ==========================
    # Job Analysis
    # ==========================
    required_skills: list[str]


    # ==========================
    # Skill Gap Analysis
    # ==========================
    missing_skills: list[str]
    match_score: float
    status: str


    # ==========================
    # Agent Outputs
    # ==========================

    # Generated when candidate is ready
    application_package: dict

    # Resume optimization suggestions
    resume_improvements: dict

    # Technical + behavioral questions
    interview_prep: dict

    # Generated when candidate is missing skills
    learning_plan: dict


    # ==========================
    # Routing
    # ==========================
    next_action: str