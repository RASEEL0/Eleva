from agents.interview_agent import interview_agent

print("Starting Interview Agent test")

state = {
    "target_job": "Backend Developer",
    "missing_skills": ["Docker", "SQL"]
}

print("Calling agent...")

result = interview_agent(state)

print("Result:")
print(result)

print("Finished") 
