from agents.resume_improvement_agent import resume_improvement_agent

print("Starting Resume Improvement Agent test")

state = {
    "target_job": "Backend Developer",
    "resume_data": {
        "skills": ["Python", "Java"],
        "experience": ["Worked on small scripts"]
    }
}

print("Calling agent...")

result = resume_improvement_agent(state)

print("Result:")
print(result)

print("Finished")
