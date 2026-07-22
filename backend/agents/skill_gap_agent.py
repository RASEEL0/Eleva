from graph.state import CareerState


def calculate_match(resume_skills, required_skills):

    resume_skills_lower = [
        skill.lower() for skill in resume_skills
    ]

    matched = []
    missing = []

    for skill in required_skills:

        if skill.lower() in resume_skills_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    score = (len(matched) / len(required_skills)) * 100

    return score, missing


def skill_gap_agent(state: CareerState):

    resume_skills = state["resume_data"].get(
        "skills", []
    )

    required_skills = state["required_skills"]


    match_score, missing_skills = calculate_match(
        resume_skills,
        required_skills
    )


    if match_score >= 80:
        next_action = "APPLICATION_READY"
        status = "Candidate matches the job requirements"

    else:
        next_action = "LEARNING_PLAN"
        status = "Candidate needs skill improvement"


    return {
        "match_score": round(match_score, 2),
        "missing_skills": missing_skills,
        "next_action": next_action,
        "status": status
    }