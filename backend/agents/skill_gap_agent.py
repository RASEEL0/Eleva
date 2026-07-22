import re

from graph.state import CareerState

GENERIC_WORDS = {
    "programming", "framework", "frameworks", "algorithm", "algorithms",
    "technique", "techniques", "system", "systems", "and", "or", "the",
    "of", "for", "tool", "tools", "integration", "deployment"
}

SYNONYMS = {
    "rest": "restful api",
    "restful": "restful api",
    "spring": "spring framework",
    "postgres": "sql",
    "postgresql": "sql",
    "mysql": "sql",
    "sqlite": "sql",
    "js": "javascript",
    "node": "node.js",
    "nodejs": "node.js",
}


def _tokenize(skill: str) -> set[str]:
    """
    Break a skill string into normalized keyword tokens, treating
    parenthetical content (often the concrete tool/tech name, e.g.
    "Version control systems (Git)") as equally important as the
    outer phrase rather than discarding it.
    """
    if not skill:
        return set()

    skill = skill.lower()
    paren_content = re.findall(r"\((.*?)\)", skill)
    skill_no_parens = re.sub(r"\(.*?\)", " ", skill)

    tokens = set()
    for piece in [skill_no_parens] + paren_content:
        piece = re.sub(r"[^a-z0-9\s,]", " ", piece)
        for part in re.split(r"[,\s]+", piece):
            part = part.strip()
            if part and len(part) > 1 and part not in GENERIC_WORDS:
                tokens.add(SYNONYMS.get(part, part))
    return tokens


def is_match(required_skill: str, resume_skills: list[str]) -> bool:
    required_tokens = _tokenize(required_skill)
    if not required_tokens:
        return False

    for resume_skill in resume_skills:
        resume_tokens = _tokenize(resume_skill)
        if resume_tokens and (resume_tokens & required_tokens):
            return True
    return False


def calculate_match(resume_skills, required_skills):
    matched = []
    missing = []

    for skill in required_skills:
        if is_match(skill, resume_skills):
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

    match_score, missing_skills = calculate_match(resume_skills, required_skills)

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