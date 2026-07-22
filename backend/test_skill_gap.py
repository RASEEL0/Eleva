from agents.skill_gap_agent import skill_gap_agent


state = {
    "resume_data": {
        "skills": [
            "Python",
            "Java",
            "RESTful APIs",
            "Git"
        ]
    },

    "required_skills": [
        "Java",
        "Python",
        "SQL",
        "RESTful APIs",
        "Docker",
        "Git",
        "Linux Shell Scripting",
        "Spring Framework"
    ]
}


result = skill_gap_agent(state)

print(result)