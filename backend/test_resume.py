print("Test file started")

from agents.resume_agent import resume_agent

print("Import successful")

state = {
    "resume_path": "test_Codes/test_files/RASEEL ALKHAMEES -EN.pdf",  
    "target_job": "Backend Developer"
}

print("Calling resume agent...")

result = resume_agent(state)

print(result)

print("Finished")