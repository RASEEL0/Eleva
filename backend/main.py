from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.career import router as career_router

app = FastAPI(
    title="Eleva",
    version="1.0.0"
)

# Allow the Lovable frontend (or the ngrok-tunneled version of this
# backend) to call this API from a different origin. Tighten
# allow_origins to your exact Lovable domain once you know it,
# instead of "*", for anything beyond local testing.
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