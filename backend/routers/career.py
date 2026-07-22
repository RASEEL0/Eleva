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


        # Resume
        "resume_text": "",

        "resume_data": {},

        "ats_score": 0,

        "strengths": [],

        "weaknesses": [],


        # Job
        "required_skills": [],


        # Skill Gap
        "missing_skills": [],

        "match_score": 0,

        "status": "",


        # Outputs
        "application_package": {},

        "resume_improvements": {},

        "interview_prep": {},

        "learning_plan": {},


        # Routing
        "next_action": ""
    }


    try:

        result = graph.invoke(initial_state)

        return result


    except Exception as e:

        return {
            "error": str(e)
        }