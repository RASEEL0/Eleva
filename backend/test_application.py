from agents.application_agent import application_agent

print("Starting Application Agent test")

state = {
    "target_job": "Backend Developer",
    "match_score": 88.5
}

print("Calling agent...")

result = application_agent(state)

print("Result:")
print(result)

print("Finished") 