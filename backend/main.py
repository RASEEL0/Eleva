from fastapi import FastAPI

from routers.career import router as career_router

app = FastAPI(
    title="Eleva",
    version="1.0.0"
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