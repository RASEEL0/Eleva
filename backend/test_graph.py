from graph.graph import build_graph


graph = build_graph()


initial_state = {

    "user_id": "1",

    "resume_path": "uploads/RASEEL ALKHAMEES -EN.pdf",

    "target_job": "Backend Developer",

    "resume_data": {},

    "required_skills": [],

    "missing_skills": [],

    "match_score": 0,

    "status": "",

    "learning_plan": {},

    "optimized_resume": "",

    "interview_questions": [],

    "next_action": ""

}


result = graph.invoke(initial_state)


print("===================")
print("FINAL STATE")
print("===================")

print(result)