from fastapi import APIRouter, UploadFile, File, Form

from graph.graph import graph


router = APIRouter()


@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    target_job: str = Form(...)
):

    file_path = f"uploads/{file.filename}"


    with open(file_path, "wb") as f:
        f.write(await file.read())


    initial_state = {

        "user_id": "demo",

        "resume_path": file_path,

        "target_job": target_job,

        "resume_text": "",

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


    return result