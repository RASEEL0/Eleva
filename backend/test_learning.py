from agents.learning_agent import learning_agent


print("Starting Learning Agent test")


state = {
    "target_job": "Backend Developer",
    "missing_skills": [
        "SQL",
        "Docker",
        "Linux Shell Scripting",
        "Spring Framework"
    ]
}


print("Calling agent...")

result = learning_agent(state)

print("Result:")
print(result)

print("Finished")