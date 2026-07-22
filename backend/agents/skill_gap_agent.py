from graph.state import CareerState


def normalize_skill(skill):

    if not skill:
        return ""

    skill = skill.lower().strip()

    replacements = {
    "rest api": "restful api",
    "restful apis": "restful api",

    "spring boot": "spring framework",
    "spring": "spring framework",

    "linux": "linux shell scripting",

    "postgres": "sql",
    "postgresql": "sql",
    "mysql": "sql",
    "sqlite": "sql",

    "js": "javascript",
    "node": "node.js"
}

    return replacements.get(skill, skill)


def calculate_match(resume_skills, required_skills):

    resume_skills_normalized = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    matched = []
    missing = []

    for skill in required_skills:

        if normalize_skill(skill) in resume_skills_normalized:
            matched.append(skill)
        else:
            missing.append(skill)

    score = (
        (len(matched) / len(required_skills)) * 100
        if required_skills else 0
    )

    return score, missing


def skill_gap_agent(state: CareerState):

    resume_skills = state["resume_data"].get("skills", [])
    required_skills = state["required_skills"]

    match_score, missing_skills = calculate_match(
        resume_skills,
        required_skills
    )

    if match_score >= 70:
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