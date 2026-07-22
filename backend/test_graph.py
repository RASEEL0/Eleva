from graph.graph import graph

initial_state = {

    "user_id": "1",

    "resume_path": "uploads/RASEEL ALKHAMEES -EN.pdf",

    "target_job": "Backend Developer",

    "resume_text": "",

    "resume_data": {},

    "ats_score": 0,

    "strengths": [],

    "weaknesses": [],

    "required_skills": [],

    "missing_skills": [],

    "match_score": 0,

    "status": "",

    "application_package": {},

    "resume_improvements": {},

    "interview_prep": {},

    "learning_plan": {},

    "next_action": ""
}


result = graph.invoke(initial_state)


print("===================")
print("FINAL STATE")
print("===================")

print(result)