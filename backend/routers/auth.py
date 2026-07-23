import secrets

from fastapi import APIRouter, Form, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import SessionLocal, User

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory session store: token -> user_id.
# Simple and fast for a capstone demo. Resets on server restart —
# if that ever matters, move this into a DB table instead.
SESSIONS = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_session(user_id: int) -> str:
    token = secrets.token_hex(16)
    SESSIONS[token] = user_id
    return token


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Use this dependency on routes that REQUIRE login (raises 401 if not logged in)."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.split(" ", 1)[1]
    user_id = SESSIONS.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_user_optional(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Use this on routes that work for both logged-in and guest users (returns None instead of raising)."""
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ", 1)[1]
    user_id = SESSIONS.get(token)
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


@router.post("/register")
def register_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(password)
    new_user = User(email=email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "email": new_user.email}


@router.post("/login")
def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_session(user.id)
    return {"message": "Login successful", "email": user.email, "token": token}


@router.post("/logout")
def logout_user(authorization: str = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        SESSIONS.pop(token, None)
    return {"message": "Logged out"}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}