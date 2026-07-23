from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers.career import router as career_router
from routers.auth import router as auth_router

app = FastAPI(
    title="Eleva",
    version="1.0.0"
)


@app.on_event("startup")
def startup_event():
    init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Eleva API is running!"
    }


app.include_router(
    career_router,
    prefix="/career",
    tags=["Career"]
)

app.include_router(
    auth_router,
    tags=["Auth"]
)