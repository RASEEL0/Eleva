import json
import os
import uuid

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from graph.graph import graph
from database import User, AnalysisResult
from routers.auth import get_current_user_optional, get_current_user, get_db

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    target_job: str = Form(...),
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Strip any directory components from the client-supplied filename and
    # prefix with a uuid so two uploads can never collide or overwrite
    # each other (e.g. "../../etc/passwd" -> "passwd").
    safe_name = os.path.basename(file.filename or "resume.pdf")
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{safe_name}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    initial_state = {
        "user_id": "demo",
        "resume_path": file_path,
        "target_job": target_job,
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

    try:
        result = graph.invoke(initial_state)

        # Only save to history if the request came from a logged-in user.
        # Guests get the same analysis, just nothing is persisted.
        if current_user is not None:
            record = AnalysisResult(
                user_id=current_user.id,
                target_job=target_job,
                match_score=result.get("match_score", 0),
                result_json=json.dumps(result)
            )
            db.add(record)
            db.commit()

        return result

    except Exception as e:
        return {"error": str(e)}


@router.get("/history")
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.user_id == current_user.id)
        .order_by(AnalysisResult.created_at.desc())
        .all()
    )
    return [
        {
            "id": r.id,
            "target_job": r.target_job,
            "match_score": r.match_score,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]


@router.get("/history/{result_id}")
def get_history_item(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.id == result_id, AnalysisResult.user_id == current_user.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Result not found")

    return json.loads(record.result_json)