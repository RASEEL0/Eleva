from agents.job_agent import job_agent

state = {
    "target_job": "Backend Developer"
}

result = job_agent(state)

print(result)